export function phb2024RollTableResultsById(source, translation) {
    if (!source || !translation || typeof translation !== "object") return source;

    const cloneOne = (r) => foundry.utils.deepClone?.(r) ?? structuredClone(r);

    if (Array.isArray(source)) {
        return source.map((result) => {
            const id = result?._id ?? result?.id;
            if (!id) return cloneOne(result);

            const patch = translation[id];
            if (!patch || typeof patch !== "object") return cloneOne(result);

            const out = cloneOne(result);
            foundry.utils.mergeObject(out, patch, {
                insertKeys: true,
                overwrite: true,
                inplace: true
            });
            return out;
        });
    }

    const out = foundry.utils.deepClone?.(source) ?? structuredClone(source);
    for (const [id, patch] of Object.entries(translation)) {
        if (!patch || typeof patch !== "object") continue;
        const target = out[id];
        if (!target || typeof target !== "object") continue;
        foundry.utils.mergeObject(target, patch, {
            insertKeys: true,
            overwrite: true,
            inplace: true
        });
    }
    return out;
}