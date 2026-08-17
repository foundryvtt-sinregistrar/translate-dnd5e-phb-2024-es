(async () => {
    // ========= CONFIG =========
    const PACK_ID = "dnd-players-handbook.tables"; // ajusta si es tables24, etc.
    const OUTPUT_FILENAME = "dnd-players-handbook.tables-en.json";
    const LABEL = "Tables";

    // ========= HELPERS =========
    const sortObjectByKeyAsc = (obj) =>
        Object.fromEntries(Object.entries(obj || {}).sort(([a], [b]) => a.localeCompare(b)));

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
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    };

    const resolvePack = (packId) => {
        const p = game.packs.get(packId);
        if (p) return p;

        const candidates = game.packs.contents
            .map((x) => x.collection)
            .filter((id) => id.includes("dnd-players-handbook") && id.includes("table"));

        throw new Error(
            `[tables-en-export] Pack not found: ${packId}\nCandidates: ${candidates.join(", ") || "(none)"}`
        );
    };

    const getTableDescription = (raw) => {
        // Algunas versiones guardan descripción en system.description.value, otras en description
        return (
            raw?.system?.description?.value ??
            raw?.system?.description ??
            raw?.description ??
            ""
        );
    };

    // ========= LOAD PACK =========
    const pack = resolvePack(PACK_ID);
    console.log(`[tables-en-export] Loading documents from: ${pack.collection}`);
    const docs = await pack.getDocuments(); // RollTable docs

    // ========= FOLDERS =========
    const folderNames = new Set();
    for (const d of docs) {
        const fname = d?.folder?.name;
        if (fname) folderNames.add(fname);
    }
    const pf = pack.folders?.contents ?? pack.folders;
    if (Array.isArray(pf)) for (const f of pf) if (f?.name) folderNames.add(f.name);

    const foldersObj = {};
    for (const name of Array.from(folderNames).sort((a, b) => a.localeCompare(b))) {
        foldersObj[name] = name; // EN export: identidad
    }

    // ========= ENTRIES =========
    const entries = {};

    for (const doc of docs) {
        const tableId = doc.id;
        const raw = doc.toObject();

        // results: array -> objeto por ID real
        const resultsArr = Array.isArray(raw?.results) ? raw.results : [];
        const resultsObj = {};

        for (const r of resultsArr) {
            const rid = r?._id ?? r?.id;
            if (!rid) continue;

            resultsObj[rid] = { text: r?.text ?? "" };
        }

        entries[tableId] = {
            name: doc.name ?? "",
            folder: doc?.folder?.name ?? "",
            description: getTableDescription(raw),
            results: sortObjectByKeyAsc(resultsObj), // SIEMPRE existe
        };
    }

    const out = {
        label: LABEL,
        mapping: {
            results: { path: "results", converter: "phb2024RollTableResultsById" },
        },
        folders: sortObjectByKeyAsc(foldersObj),
        entries: sortObjectByKeyAsc(entries),
    };

    // ========= EXPORT =========
    downloadText(JSON.stringify(out, null, 2), OUTPUT_FILENAME);

    console.log(`[tables-en-export] Done. Downloaded: ${OUTPUT_FILENAME}`);
    console.table({
        entries: Object.keys(out.entries).length,
        folders: Object.keys(out.folders).length,
    });
})();