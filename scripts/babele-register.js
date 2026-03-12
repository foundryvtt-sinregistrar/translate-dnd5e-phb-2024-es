/**
 * Babele registration for this translation module.
 * - Registers for both "es" and "es-ES" style language codes.
 */
Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele) return;

  const current = game.i18n?.lang ?? "es";
  const base = current.split("-")[0];
  const langs = Array.from(new Set([current, base]));

    const compendium = {
        "dnd-players-handbook.actors": {
            label: "PHB 2024 - Actores",
            path: "dnd-players-handbook.actors.json"
        },
        "dnd-players-handbook.classes": {
            label: "PHB 2024 - Clases",
            path: "dnd-players-handbook.classes.json"
        },
        "dnd-players-handbook.content": {
            label: "PHB 2024 - Contenido",
            path: "dnd-players-handbook.content.json"
        },
        "dnd-players-handbook.equipment": {
            label: "PHB 2024 - Equipo",
            path: "dnd-players-handbook.equipment.json"
        },
        "dnd-players-handbook.feats": {
            label: "PHB 2024 - Dotes",
            path: "dnd-players-handbook.feats.json"
        },
        "dnd-players-handbook.origins": {
            label: "PHB 2024 - Orígenes",
            path: "dnd-players-handbook.origins.json"
        },
        "dnd-players-handbook.spells": {
            label: "PHB 2024 - Conjuros",
            path: "dnd-players-handbook.spells.json"
        },
        "dnd-players-handbook.tables": {
            label: "PHB 2024 - Tablas",
            path: "dnd-players-handbook.tables.json"
        }
    };

    for (const lang of langs) {
        try {
            babele.register({
                module: "translate-dnd5e-phb-2024-es",
                lang,
                dir: "compendium",
                compendium
            });

            console.log(
                `[Babele - translate-dnd5e-phb-2024-es] Registered ${Object.keys(compendium).length} compendiums for lang="${lang}" (dir=compendium)`
            );
        } catch (err) {
            console.error(
                `[Babele - translate-dnd5e-phb-2024-es] Failed registering for lang="${lang}"`,
                err
            );
        }
    }
});