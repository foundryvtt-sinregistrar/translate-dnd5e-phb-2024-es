export function phb2024AdvancementById(source, translation) {
  if (!source || typeof source !== "object" || !translation || typeof translation !== "object") return source;
  const result = foundry.utils.deepClone(source);
  const patches = Array.isArray(translation)
    ? Object.fromEntries(translation.filter(value => value?._id ?? value?.id).map(value => [value._id ?? value.id, value]))
    : translation;
  const rows = Array.isArray(result.contents) ? result.contents : result;
  for (const [key, advancement] of Object.entries(rows)) {
    if (!advancement || typeof advancement !== "object" || Array.isArray(advancement)) continue;
    const id = advancement._id ?? advancement.id ?? key;
    const patch = Object.hasOwn(patches, id) ? patches[id] : undefined;
    if (!patch || typeof patch !== "object" || Array.isArray(patch)) continue;
    const label = typeof patch.name === "string" ? patch.name : patch.title;
    if (typeof label === "string") advancement["name" in advancement ? "name" : "title"] = label;
    if (typeof patch.hint === "string") advancement.hint = patch.hint;
  }
  return result;
}
