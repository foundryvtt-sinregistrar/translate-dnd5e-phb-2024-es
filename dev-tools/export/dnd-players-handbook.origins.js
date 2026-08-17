(async () => {
    const PACK_ID = "dnd-players-handbook.origins";
    const OUTPUT_FILENAME = "dnd-players-handbook.origins-en.v3.json";
    const LABEL = "Origins";

    try {
        const isDigitFirst = (value) => /^\d/.test(String(value || ""));

        const compareIdsAscNumericFirst = (a, b) => {
            const aStr = String(a ?? "");
            const bStr = String(b ?? "");

            const aNum = isDigitFirst(aStr);
            const bNum = isDigitFirst(bStr);

            if (aNum !== bNum) return aNum ? -1 : 1;
            return aStr.localeCompare(bStr, undefined, { numeric: true, sensitivity: "base" });
        };

        const sortObjectByKeyAscNumericFirst = (obj) =>
            Object.fromEntries(
                Object.entries(obj || {}).sort(([a], [b]) => compareIdsAscNumericFirst(a, b))
            );

        const reorderEntryForFinalOutput = (entry) => ({
            name: entry?.name ?? "",
            description: entry?.description ?? "",
            folder: entry?.folder ?? "",
            activities: sortObjectByKeyAscNumericFirst(entry?.activities || {}),
            effects: sortObjectByKeyAscNumericFirst(entry?.effects || {}),
            advancement: sortObjectByKeyAscNumericFirst(entry?.advancement || {})
        });

        const toArray = (value) => {
            if (!value) return [];
            if (Array.isArray(value)) return value;
            if (Array.isArray(value?.contents)) return value.contents;
            if (typeof value?.[Symbol.iterator] === "function") return Array.from(value);
            if (typeof value === "object") return Object.values(value);
            return [];
        };

        const firstDefined = (...values) =>
            values.find(
                (v) => v !== undefined && v !== null && !(typeof v === "string" && v === "")
            );

        const safeString = (v) => (typeof v === "string" ? v : "");
        const hasValue = (v) =>
            v !== undefined && v !== null && !(typeof v === "string" && v === "");

        const humanize = (value) => {
            if (!value || typeof value !== "string") return "";
            return value
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/[_\-./]+/g, " ")
                .replace(/\s+/g, " ")
                .trim()
                .replace(/\b\w/g, (m) => m.toUpperCase());
        };

        const downloadText = (text, filename) => {
            if (typeof saveDataToFile === "function") {
                saveDataToFile(text, "text/json", filename);
                return;
            }

            const blob = new Blob([text], { type: "application/json" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        };

        const getFolderId = (folder) =>
            firstDefined(folder?.id, folder?._id, typeof folder === "string" ? folder : undefined);

        const getFolderName = (doc, folderById) => {
            const folder = doc?.folder;
            if (!folder) return "";

            if (typeof folder === "string") return folderById.get(folder) ?? folder;
            if (typeof folder?.name === "string" && folder.name) return folder.name;

            const id = getFolderId(folder);
            if (id) return folderById.get(id) ?? "";

            return "";
        };

        const getDescription = (doc) => {
            const raw = firstDefined(
                doc?.system?.description?.value,
                doc?.system?.description,
                doc?.description?.value,
                doc?.description,
                doc?.system?.details?.biography?.value,
                doc?.system?.details?.biography
            );
            return safeString(raw);
        };

        const getEffectDescription = (effect) => {
            const raw = firstDefined(
                effect?.description,
                effect?.system?.description?.value,
                effect?.system?.description,
                effect?.flags?.dae?.description
            );
            return safeString(raw);
        };

        const getActivityName = (act) => {
            const direct = firstDefined(
                act?.name,
                act?.label,
                act?.title,
                act?.typeLabel,
                act?.metadata?.title,
                act?.metadata?.name,
                act?.usage?.label,
                act?.chatFlavor
            );
            if (typeof direct === "string" && direct.trim()) return direct.trim();

            const type = safeString(
                firstDefined(act?.type, act?.activityType, act?.metadata?.type)
            ).toLowerCase();

            const typeMap = {
                attack: "Attack",
                save: "Save",
                damage: "Damage",
                heal: "Heal",
                summon: "Summon",
                utility: "Utility",
                cast: "Cast",
                check: "Check",
                enchant: "Enchant",
                consume: "Consume",
                move: "Move",
                teleport: "Teleport"
            };

            if (type && typeMap[type]) return typeMap[type];

            return "";
        };

        const getActivityTarget = (act) => {
            const target = firstDefined(
                act?.target,
                act?.targets,
                act?.consumption?.target
            );

            if (typeof target === "string") return target;

            const special = firstDefined(
                target?.special,
                target?.prompt,
                target?.label,
                target?.affects?.special,
                act?.target?.affects?.special
            );
            if (typeof special === "string" && special.trim()) return special.trim();

            const templateType = safeString(firstDefined(target?.template?.type, target?.type));
            const templateSize = firstDefined(target?.template?.size, target?.value, target?.count);

            if (templateType && hasValue(templateSize)) return `${templateSize} ${templateType}`;
            if (templateType) return templateType;

            return "";
        };

        const getActivityCondition = (act) =>
            safeString(
                firstDefined(
                    act?.activation?.condition,
                    act?.condition,
                    act?.trigger?.condition,
                    act?.uses?.condition,
                    act?.usage?.condition
                )
            );

        const getActivityChatFlavor = (act) =>
            safeString(
                firstDefined(
                    act?.description?.chatFlavor,
                    act?.chatFlavor
                )
            );

        const serializeActivities = (item) => {
            const out = {};
            const activities = item?.system?.activities;

            for (const act of toArray(activities)) {
                const id = firstDefined(act?._id, act?.id);
                if (!id) continue;

                const patch = {};

                const name = getActivityName(act);
                if (name !== "") patch.name = name;

                const target = getActivityTarget(act);
                if (target !== "") patch.target = target;

                const condition = getActivityCondition(act);
                if (condition !== "") patch.activation = { condition };

                const chatFlavor = getActivityChatFlavor(act);
                if (chatFlavor !== "") patch.description = { chatFlavor };

                out[id] = patch;
            }

            return sortObjectByKeyAscNumericFirst(out);
        };

        const serializeEffects = (doc) => {
            const out = {};

            for (const eff of toArray(doc?.effects)) {
                const id = firstDefined(eff?._id, eff?.id);
                if (!id) continue;

                const patch = {};

                if (typeof eff?.name === "string" && eff.name) patch.name = eff.name;

                const description = getEffectDescription(eff);
                if (description !== "") patch.description = description;

                out[id] = patch;
            }

            return sortObjectByKeyAscNumericFirst(out);
        };

        const getAdvancementTitle = (adv, item) => {
            const direct = firstDefined(
                adv?.title,
                adv?.configuration?.title,
                adv?.configuration?.label,
                adv?.configuration?.name,
                adv?.value?.title,
                adv?.value?.label,
                adv?.label,
                adv?.name,
                adv?.typeLabel
            );
            if (typeof direct === "string" && direct.trim()) return direct.trim();

            const identifier = firstDefined(
                adv?.configuration?.identifier,
                adv?.configuration?.scale?.identifier,
                adv?.identifier,
                adv?.value?.identifier
            );
            if (typeof identifier === "string" && identifier.trim()) {
                return humanize(identifier);
            }

            const type = safeString(firstDefined(adv?.type, adv?.constructor?.name)).toLowerCase();
            const itemType = safeString(item?.type).toLowerCase();

            if (type.includes("abilityscore")) return "Ability Score Improvement";
            if (type.includes("scale")) return humanize(identifier || "Scale Value");
            if (type.includes("itemgrant") || type.includes("itemchoice")) {
                return itemType === "subclass" ? "Subclass Features" : "Class Features";
            }
            if (type.includes("trait")) return humanize(identifier || "Traits");
            if (type.includes("hitpoint")) return "Hit Points";
            if (type.includes("size")) return "Size";

            return "";
        };

        const getAdvancementHint = (adv) =>
            safeString(
                firstDefined(
                    adv?.hint,
                    adv?.configuration?.hint,
                    adv?.value?.hint
                )
            );

        const serializeAdvancement = (item) => {
            const out = {};

            for (const adv of toArray(item?.system?.advancement)) {
                const id = firstDefined(adv?._id, adv?.id);
                if (!id) continue;

                const patch = {};

                const title = getAdvancementTitle(adv, item);
                if (title !== "") patch.title = title;

                const hint = getAdvancementHint(adv);
                if (hint !== "") patch.hint = hint;

                out[id] = patch;
            }

            return sortObjectByKeyAscNumericFirst(out);
        };

        const pack = game.packs.get(PACK_ID);
        if (!pack) throw new Error(`No se encontró el pack: ${PACK_ID}`);

        await pack.getIndex();
        const docs = await pack.getDocuments();

        const folderById = new Map();

        for (const folder of toArray(pack?.folders)) {
            const id = getFolderId(folder);
            const name = safeString(folder?.name);
            if (id && name) folderById.set(id, name);
        }

        for (const item of docs) {
            const folder = item?.folder;
            const id = getFolderId(folder);
            const name = safeString(folder?.name);
            if (id && name) folderById.set(id, name);
        }

        const folderNames = Array.from(
            new Set([
                ...toArray(pack?.folders).map((f) => safeString(f?.name)).filter(Boolean),
                ...docs.map((item) => getFolderName(item, folderById)).filter(Boolean)
            ])
        ).sort((a, b) => a.localeCompare(b));

        const folders = Object.fromEntries(folderNames.map((name) => [name, name]));

        const entries = {};
        for (const item of docs) {
            const id = firstDefined(item?._id, item?.id);
            if (!id) continue;

            entries[id] = {
                name: safeString(item?.name),
                description: getDescription(item),
                folder: getFolderName(item, folderById),
                activities: serializeActivities(item),
                effects: serializeEffects(item),
                advancement: serializeAdvancement(item)
            };
        }

        const orderedEntries = Object.fromEntries(
            Object.entries(entries)
                .sort(([a], [b]) => compareIdsAscNumericFirst(a, b))
                .map(([id, entry]) => [id, reorderEntryForFinalOutput(entry)])
        );

        const output = {
            label: LABEL,
            mapping: {
                activities: {
                    path: "system.activities",
                    converter: "phb2024ActivitiesById"
                },
                effects: {
                    path: "effects",
                    converter: "phb2024MergeEffects"
                },
                advancement: {
                    path: "system.advancement",
                    converter: "phb2024AdvancementById"
                }
            },
            folders: sortObjectByKeyAscNumericFirst(folders),
            entries: orderedEntries
        };

        const json = JSON.stringify(output, null, 2);
        downloadText(json, OUTPUT_FILENAME);

        let emptyActivityNames = 0;
        let emptyAdvancementTitles = 0;

        for (const entry of Object.values(output.entries)) {
            for (const act of Object.values(entry.activities || {})) {
                if (!safeString(act?.name)) emptyActivityNames++;
            }
            for (const adv of Object.values(entry.advancement || {})) {
                if (!safeString(adv?.title)) emptyAdvancementTitles++;
            }
        }

        console.log(`[OK] Exportado ${OUTPUT_FILENAME}`, {
            pack: PACK_ID,
            entries: Object.keys(output.entries).length,
            folders: Object.keys(output.folders).length,
            emptyActivityNames,
            emptyAdvancementTitles
        });

        return output;
    } catch (error) {
        console.error("[ERROR] No se pudo exportar " + OUTPUT_FILENAME, error);
    }
})();