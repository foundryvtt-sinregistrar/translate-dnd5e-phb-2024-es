/**
 * phb2024ActorDetails
 * - Aplica traducción al bloque system.details del Actor
 * - Pensado para mapping:
 *   "details": { "path": "system.details", "converter": "phb2024ActorDetails" }
 */
export function phb2024ActorDetails(source, translation) {
    if (!source || typeof source !== "object" || !translation || typeof translation !== "object") {
        return source;
    }

    const out = foundry.utils.deepClone(source);

    const fields = [
        "alignment",
        "eyes",
        "height",
        "faith",
        "hair",
        "weight",
        "gender",
        "skin",
        "age",
        "ideal",
        "bond",
        "flaw",
        "trait",
        "appearance"
    ];

    for (const key of fields) {
        if (translation[key] !== undefined) {
            out[key] = translation[key];
        }
    }

    return out;
}
