export function phb2024ActivitiesById(source, translation) {
    if (!source || typeof source !== "object" || !translation || typeof translation !== "object") {
        return source;
    }

    const out = foundry.utils.deepClone(source);

    for (const [actId, act] of Object.entries(out)) {
        const patch = translation[actId];
        if (!patch || typeof patch !== "object") continue;

        foundry.utils.mergeObject(act, patch, {
            insertKeys: true,
            overwrite: true,
            inplace: true
        });
    }

    return out;
}