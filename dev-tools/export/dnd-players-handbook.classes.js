(async () => {
    /**
     * =========================================
     * V4 - Classes Export
     * =========================================
     * Criterios:
     * - ❌ Sin ordenación por folder
     * - ✅ entries: ordenación alfabética ASC por entryId, números primero y luego letras
     * - ✅ activities: ordenación alfabética ASC por activityId, números primero y luego letras
     * - ✅ effects: ordenación alfabética ASC por effectId, números primero y luego letras
     * - ✅ advancement: ordenación alfabética ASC por advancementId, números primero y luego letras
     * - ❌ Sin range
     * - ❌ Sin duration
     */

    const PACK_ID = "dnd-players-handbook.classes";
    const OUTPUT_FILENAME = "dnd-players-handbook.classes-en.json";
    const LABEL = "Character Classes";

    try {
        const getLeadingGroupRank = (key) => {
            const value = typeof key === "string" ? key.trim() : "";
            if (!value) return 2;

            const first = value.charAt(0);

            if (/[0-9]/.test(first)) return 0;    // números primero
            if (/[A-Za-z]/.test(first)) return 1; // letras después
            return 2;                             // resto al final
        };

        const compareAlphaAscNumbersFirst = (a, b) => {
            const rankA = getLeadingGroupRank(a);
            const rankB = getLeadingGroupRank(b);

            if (rankA !== rankB) {
                return rankA - rankB;
            }

            return String(a).localeCompare(String(b), undefined, {
                sensitivity: "base",
                numeric: false
            });
        };

        const sortObjectByAlphaAscNumbersFirst = (obj) =>
            Object.fromEntries(
                Object.entries(obj || {}).sort(([a], [b]) =>
                    compareAlphaAscNumbersFirst(a, b)
                )
            );

        const sortEntriesByIdAlphaAscNumbersFirst = (entriesObj) =>
            Object.fromEntries(
                Object.entries(entriesObj || {}).sort(([idA], [idB]) =>
                    compareAlphaAscNumbersFirst(idA, idB)
                )
            );

        const reorderEntryForFinalOutput = (entry) => ({
            name: entry?.name ?? "",
            description: entry?.description ?? "",
            folder: entry?.folder ?? "",
            activities: sortObjectByAlphaAscNumbersFirst(entry?.activities || {}),
            effects: sortObjectByAlphaAscNumbersFirst(entry?.effects || {}),
            advancement: sortObjectByAlphaAscNumbersFirst(entry?.advancement || {})
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

            return typeMap[type] ?? "";
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

            return typeof special === "string" ? special.trim() : "";
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
                if (chatFlavor !== "") {
                    patch.description = { chatFlavor };
                }

                out[id] = patch;
            }

            return sortObjectByAlphaAscNumbersFirst(out);
        };

        const serializeEffects = (doc) => {
            const out = {};

            for (const eff of toArray(doc?.effects)) {
                const id = firstDefined(eff?._id, eff?.id);
                if (!id) continue;

                const patch = {};

                if (eff?.name) patch.name = eff.name;

                const description = getEffectDescription(eff);
                if (description !== "") patch.description = description;

                out[id] = patch;
            }

            return sortObjectByAlphaAscNumbersFirst(out);
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

            if (identifier) return humanize(identifier);

            const type = safeString(firstDefined(adv?.type)).toLowerCase();

            if (type.includes("abilityscore")) return "Ability Score Improvement";
            if (type.includes("itemgrant")) return "Class Features";

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

            return sortObjectByAlphaAscNumbersFirst(out);
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
            Object.entries(sortEntriesByIdAlphaAscNumbersFirst(entries)).map(([id, entry]) => [
                id,
                reorderEntryForFinalOutput(entry)
            ])
        );

        const output = {
            label: LABEL,
            mapping: {
                activities: { path: "system.activities", converter: "phb2024ActivitiesById" },
                effects: { path: "effects", converter: "phb2024MergeEffects" },
                advancement: { path: "system.advancement", converter: "phb2024AdvancementById" }
            },
            entries: orderedEntries
        };

        downloadText(JSON.stringify(output, null, 2), OUTPUT_FILENAME);

        console.log("[OK] V4 export generado correctamente", {
            entryOrder: "ordenacion alphabetica ASC by entryId, primero numeros y luego letras",
            activityOrder: "ordenacion alphabetica ASC by activityId, primero numeros y luego letras",
            effectOrder: "ordenacion alphabetica ASC by effectId, primero numeros y luego letras",
            advancementOrder: "ordenacion alphabetica ASC by advancementId, primero numeros y luego letras",
            range: "excluded",
            duration: "excluded"
        });

        return output;

    } catch (error) {
        console.error("[ERROR] V4 fallo", error);
    }
})();