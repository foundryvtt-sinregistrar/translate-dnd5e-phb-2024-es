(async () => {
    // ========= CONFIG =========
    const PACK_ID = "dnd-players-handbook.content"; // cambia si tu pack se llama distinto
    const OUTPUT_FILENAME = "dnd-players-handbook.content-en.json";
    const LABEL = "Content";

    // Exportar campos extra por página (normalmente NO hace falta para Babele)
    const EXPORT_PAGE_TYPE = true;   // page.type
    const EXPORT_PAGE_SRC  = true;   // page.src (si existe, páginas imagen/video)
    const EXPORT_PAGE_FLAGS = false; // page.flags (muy grande/ruidoso)

    // ========= HELPERS =========
    const isPlainObject = (v) => v && typeof v === "object" && !Array.isArray(v);

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

        // Fallback: intenta encontrar algo parecido
        const candidates = game.packs.contents
            .map((x) => x.collection)
            .filter((id) => id.includes("dnd-players-handbook") && id.includes("content"));

        throw new Error(
            `[content-en-export] Pack not found: ${packId}\n` +
            `Candidates: ${candidates.join(", ") || "(none)"}`
        );
    };

    // ========= LOAD PACK =========
    const pack = resolvePack(PACK_ID);
    console.log(`[content-en-export] Loading documents from: ${pack.collection}`);
    const docs = await pack.getDocuments(); // JournalEntry docs

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
        const entryId = doc.id;

        // Pages: usar IDs reales como keys (NO usar page.name)
        const pagesOut = {};
        const pages = doc.pages?.contents ?? doc.pages ?? [];
        for (const p of pages) {
            const pageId = p.id;
            const raw = p.toObject();

            const outPage = {
                name: p.name ?? "",
                // contenido HTML (la mayoría de páginas PHB son "text")
                text: raw?.text?.content ?? raw?.text ?? "",
            };

            if (EXPORT_PAGE_TYPE) outPage.type = raw?.type ?? p.type ?? "";
            if (EXPORT_PAGE_SRC && (raw?.src ?? p.src)) outPage.src = raw?.src ?? p.src;
            if (EXPORT_PAGE_FLAGS && isPlainObject(raw?.flags)) outPage.flags = raw.flags;

            pagesOut[pageId] = outPage;
        }

        entries[entryId] = {
            name: doc.name ?? "",
            folder: doc?.folder?.name ?? "",
            pages: sortObjectByKeyAsc(pagesOut), // SIEMPRE existe
        };
    }

    const out = {
        label: LABEL,
        mapping: {
            // Lo típico para content/journal:
            pages: { path: "pages", converter: "phb2024JournalPagesById" },
            // Si usas el converter "full", puedes cambiarlo aquí:
            // entry: { path: "", converter: "phb2024JournalEntryFullById" }
        },
        folders: sortObjectByKeyAsc(foldersObj),
        entries: sortObjectByKeyAsc(entries),
    };

    // ========= EXPORT =========
    downloadText(JSON.stringify(out, null, 2), OUTPUT_FILENAME);

    console.log(`[content-en-export] Done. Downloaded: ${OUTPUT_FILENAME}`);
    console.table({
        entries: Object.keys(out.entries).length,
        folders: Object.keys(out.folders).length,
    });
})();