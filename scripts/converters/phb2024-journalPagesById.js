export function phb2024JournalPagesById(source, translation) {
    if (!source || !translation) return source;

    // Normaliza colección de páginas
    const pages = (() => {
        if (Array.isArray(source)) return source;
        if (Array.isArray(source?.contents)) return source.contents;
        if (typeof source?.[Symbol.iterator] === "function") return Array.from(source);
        if (typeof source === "object") return Object.values(source);
        return [];
    })();

    const tPages = translation;

    for (const page of pages) {
        const pageId = page?._id ?? page?.id;
        if (!pageId) continue;

        const tPage = tPages[pageId];
        if (!tPage) continue;

        // Nombre de página
        if (typeof tPage.name === "string") page.name = tPage.name;

        // TEXT: soporta string o text.content
        const textContent =
            (typeof tPage.text === "string") ? tPage.text :
                (tPage.text?.content !== undefined) ? tPage.text.content :
                    undefined;

        if (textContent !== undefined) {
            if (typeof page.text === "string") {
                page.text = textContent;
            } else {
                page.text = page.text ?? {};
                if (typeof page.text === "object") {
                    page.text.content = textContent;
                    if (page.text.format === undefined) page.text.format = 1;
                }
            }

            page.system = page.system ?? {};
            page.system.text = page.system.text ?? {};
            if (typeof page.system.text === "object") {
                page.system.text.content = textContent;
            }
        }

        // DESCRIPTION: soporta string o description.value
        const descValue =
            (typeof tPage.description === "string") ? tPage.description :
                (tPage.description?.value !== undefined) ? tPage.description.value :
                    undefined;

        if (descValue !== undefined) {
            page.system = page.system ?? {};
            page.system.description = page.system.description ?? {};
            if (typeof page.system.description === "object") {
                page.system.description.value = descValue;
            }
        }

        // subclassHeader
        if (tPage.subclassHeader !== undefined) {
            page.system = page.system ?? {};
            page.system.subclassHeader = tPage.subclassHeader;
        }

        // subclass
        const subclassValue =
            (typeof tPage.subclass === "string") ? tPage.subclass :
                (tPage.description?.subclass !== undefined) ? tPage.description.subclass :
                    undefined;

        if (subclassValue !== undefined) {
            page.system = page.system ?? {};
            page.system.description = page.system.description ?? {};
            if (typeof page.system.description === "object") {
                page.system.description.subclass = subclassValue;
            }
        }
    }

    return source;
}