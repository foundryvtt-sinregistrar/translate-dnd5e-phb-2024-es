// dnd-players-handbook.classes.json id phbbrbBrutalStri
(async () => {
    const packId = "dnd-players-handbook.content";
    const docId  = "phbPlayingTheGam";

    try {
        const pack = game.packs.get(packId);
        if (!pack) return ui.notifications.error(`No encuentro el pack: ${packId}`);

        const doc = await pack.getDocument(docId);
        if (!doc) return ui.notifications.error(`No encuentro el documento: ${docId}`);

        const data = doc.toObject();
        const json = JSON.stringify(data, null, 2);

        const fileName = `${packId.replace(/[^\w.-]+/g, "_")}.${docId}.json`;

        // ✅ Método nativo Foundry (si existe)
        if (globalThis.foundry?.utils?.saveDataToFile) {
            foundry.utils.saveDataToFile(json, "application/json", fileName);
        } else {
            // ✅ Fallback: descarga por Blob (funciona en cualquier navegador)
            const blob = new Blob([json], { type: "application/json;charset=utf-8" });
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            a.remove();

            URL.revokeObjectURL(url);
        }

        // (Opcional) copiar también al portapapeles
        // await navigator.clipboard.writeText(json);

        console.log(data);
        ui.notifications.info(`JSON descargado: ${fileName}`);
    } catch (err) {
        console.error(err);
        ui.notifications.error(`Error exportando ${packId}.${docId}: ${err?.message ?? err}`);
    }
})();