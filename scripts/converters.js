

import { phb2024MergeEffects } from "./converters/phb2024-merge-effects.js";
import { phb2024AdvancementById } from "./converters/phb2024-advancement-by-id.js";
import { phb2024JournalPagesById } from "./converters/phb2024-journalPagesById.js";
import { phb2024JournalEntryFullById } from "./converters/phb2024-journalEntryFullById.js";
import { phb2024ActorFullById } from "./converters/phb2024-actorFullById.js";
import { phb2024RollTableResultsById } from "./converters/phb2024-rollTableResultsById.js";
import { phb2024ActivitiesById } from "./converters/phb2024-activities-by-id.js";


Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele?.registerConverters) return;

    babele.registerConverters({
        phb2024ActivitiesById,
        phb2024MergeEffects,
        phb2024AdvancementById,
        phb2024JournalPagesById,
        phb2024JournalEntryFullById,
        phb2024ActorFullById,
        phb2024RollTableResultsById
    });

    console.log("[Babele - translate-dnd5e-phb-2024-es] Converters registered:", Object.keys(babele.converters ?? {}));
});