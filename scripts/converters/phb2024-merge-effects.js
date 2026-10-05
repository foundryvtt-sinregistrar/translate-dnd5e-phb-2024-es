export function phb2024MergeEffects(source, translation) {
  if (!source || typeof source !== "object" || !translation || typeof translation !== "object") return source;

  const byId = {};
  const byName = {};

  if (Array.isArray(translation)) {
    for (const t of translation) {
      if (!t) continue;
      if (t._id) byId[t._id] = t;
      if (t.name && !t._id) byName[t.name] = t;
    }
  } else if (typeof translation === "object") {
    for (const [k, v] of Object.entries(translation)) {
      if (!v || typeof v !== "object") continue;
      const id = v._id || k;
      if (typeof id === "string" && id.length >= 6 && (id === v._id || /^[a-zA-Z0-9]{6,}$/.test(id))) {
        byId[id] = v;
      }
      if (typeof k === "string") byName[k] = v;
    }
  }

  const deepClone =
    globalThis.foundry?.utils?.deepClone
      ? foundry.utils.deepClone
      : structuredClone;
  const out = deepClone(source);
  const rows = Array.isArray(out.contents) ? out.contents : out;

  for (const [key, eff] of Object.entries(rows)) {
    if (!eff || typeof eff !== "object" || Array.isArray(eff)) continue;
    const id = eff._id ?? eff.id ?? key;
    const name = eff?.name;

    const patch = (id && byId[id]) ? byId[id] : (name && byName[name]) ? byName[name] : null;
    if (!patch) continue;
    if (typeof patch.name === "string") eff.name = patch.name;
    if (typeof patch.description === "string") eff.description = patch.description;
  }
  return out;
}
