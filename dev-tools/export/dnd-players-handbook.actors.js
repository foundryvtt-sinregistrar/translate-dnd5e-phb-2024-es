(async () => {
    // ============================================================
    // EXPORT PHB 2024 ACTORS (EN) - V6
    // - Mantiene formato slim de actors-en.v5.json
    // - Incluye bloque top-level `details`
    // - NO exporta activities.*.range
    // - NO exporta activities.*.duration
    // ============================================================

    const PACK_ID = "dnd-players-handbook.actors";
    const OUTPUT_FILENAME = "dnd-players-handbook.actors-en.json";
    const LABEL = "Actors";

    const isPlainObject = (v) => v && typeof v === "object" && !Array.isArray(v);
    const ensurePlainObject = (v) => (isPlainObject(v) ? v : {});

    const getPropertySafe = (obj, path, fallback = undefined) => {
        try {
            if (!obj || !path) return fallback;
            if (foundry?.utils?.getProperty) {
                const value = foundry.utils.getProperty(obj, path);
                return value === undefined ? fallback : value;
            }
            const value = path.split(".").reduce((acc, key) => (acc == null ? undefined : acc[key]), obj);
            return value === undefined ? fallback : value;
        } catch {
            return fallback;
        }
    };

    const toText = (value) => {
        if (value === null || value === undefined) return "";
        if (typeof value === "string") return value;
        if (typeof value === "number" || typeof value === "boolean") return String(value);
        return "";
    };

    const smartCompare = (a, b) => String(a).localeCompare(String(b), undefined, {
        numeric: true,
        sensitivity: "base"
    });

    const sortObjectByKeyAsc = (obj) => {
        const entries = Object.entries(ensurePlainObject(obj)).sort(([a], [b]) => smartCompare(a, b));
        return Object.fromEntries(entries);
    };

    const arrayToSortedObjectById = (arr, mapper) => {
        const items = Array.isArray(arr) ? [...arr] : [];
        items.sort((a, b) => smartCompare(a?._id ?? a?.id ?? "", b?._id ?? b?.id ?? ""));
        return Object.fromEntries(
            items
                .map((item) => {
                    const id = item?._id ?? item?.id;
                    if (!id) return null;
                    return [id, mapper(item)];
                })
                .filter(Boolean)
        );
    };

    const compactObject = (obj) => {
        const out = {};
        for (const [k, v] of Object.entries(ensurePlainObject(obj))) {
            if (v === undefined) continue;
            out[k] = v;
        }
        return out;
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
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 1500);
    };

    const extractActivity = (activity) => {
        const out = {
            name: toText(activity?.name)
        };

        const condition = getPropertySafe(activity, "activation.condition", "");
        const chatFlavor = getPropertySafe(activity, "description.chatFlavor", "");

        if (toText(condition) !== "") out.condition = toText(condition);
        if (toText(chatFlavor) !== "") out.chatFlavor = toText(chatFlavor);

        return out;
    };

    const extractEffect = (effect) => {
        return {
            name: toText(effect?.name),
            description: toText(effect?.description ?? getPropertySafe(effect, "description.value", ""))
        };
    };

    const extractAdvancement = (adv) => {
        return compactObject({
            title: toText(adv?.title),
            hint: toText(adv?.hint)
        });
    };

    const extractItem = (item) => {
        const activities = sortObjectByKeyAsc(
            Object.fromEntries(
                Object.entries(ensurePlainObject(getPropertySafe(item, "system.activities", {})))
                    .sort(([a], [b]) => smartCompare(a, b))
                    .map(([id, activity]) => [id, extractActivity(activity)])
            )
        );

        const effects = arrayToSortedObjectById(getPropertySafe(item, "effects", []), extractEffect);
        const advancement = arrayToSortedObjectById(getPropertySafe(item, "system.advancement", []), extractAdvancement);

        return {
            name: toText(item?.name),
            description: toText(getPropertySafe(item, "system.description.value", item?.description ?? "")),
            activities,
            effects,
            advancement
        };
    };

    const extractActorDetails = (actorObj) => {
        return {
            alignment: toText(getPropertySafe(actorObj, "system.details.alignment", "")),
            eyes: toText(getPropertySafe(actorObj, "system.details.eyes", "")),
            height: toText(getPropertySafe(actorObj, "system.details.height", "")),
            faith: toText(getPropertySafe(actorObj, "system.details.faith", "")),
            hair: toText(getPropertySafe(actorObj, "system.details.hair", "")),
            weight: toText(getPropertySafe(actorObj, "system.details.weight", "")),
            gender: toText(getPropertySafe(actorObj, "system.details.gender", "")),
            skin: toText(getPropertySafe(actorObj, "system.details.skin", "")),
            age: toText(getPropertySafe(actorObj, "system.details.age", "")),
            ideal: toText(getPropertySafe(actorObj, "system.details.ideal", "")),
            bond: toText(getPropertySafe(actorObj, "system.details.bond", "")),
            flaw: toText(getPropertySafe(actorObj, "system.details.flaw", "")),
            trait: toText(getPropertySafe(actorObj, "system.details.trait", "")),
            appearance: toText(getPropertySafe(actorObj, "system.details.appearance", ""))
        };
    };

    const extractActor = (doc) => {
        const actor = doc.toObject();

        return {
            name: toText(actor?.name),
            description: toText(getPropertySafe(actor, "system.description.value", getPropertySafe(actor, "system.details.biography.value", ""))),
            folder: toText(doc?.folder?.name ?? ""),
            biography: toText(getPropertySafe(actor, "system.details.biography.value", "")),
            details: extractActorDetails(actor),
            effects: arrayToSortedObjectById(getPropertySafe(actor, "effects", []), extractEffect),
            items: arrayToSortedObjectById(getPropertySafe(actor, "items", []), extractItem)
        };
    };

    const pack = game.packs.get(PACK_ID);
    if (!pack) {
        ui.notifications.error(`Pack no encontrado: ${PACK_ID}`);
        return;
    }

    const docs = await pack.getDocuments();
    const folders = (pack.folders?.contents ?? pack.folders ?? []).map((f) => f?.name).filter(Boolean).sort(smartCompare);

    const output = {
        label: LABEL,
        mapping: {
            details: {
                path: "system.details",
                converter: "phb2024ActorDetails"
            },
            items: {
                path: "items",
                converter: "phb2024ActorFullById"
            }
        },
        folders: Object.fromEntries(folders.map((name) => [name, name])),
        entries: Object.fromEntries(
            [...docs]
                .sort((a, b) => smartCompare(a.id ?? a._id ?? "", b.id ?? b._id ?? ""))
                .map((doc) => [doc.id ?? doc._id, extractActor(doc)])
        )
    };

    const json = JSON.stringify(output, null, 2);
    console.log(`[${PACK_ID}] Export completado:`, {
        docs: docs.length,
        folders: folders.length,
        filename: OUTPUT_FILENAME
    });
    downloadText(json, OUTPUT_FILENAME);
})();
