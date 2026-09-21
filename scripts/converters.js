import {phb2024MergeEffects} from "./converters/phb2024-merge-effects.js";
import {phb2024AdvancementById} from "./converters/phb2024-advancement-by-id.js";
import {phb2024JournalPagesById} from "./converters/phb2024-journalPagesById.js";
import {phb2024JournalEntryFullById} from "./converters/phb2024-journalEntryFullById.js";
import {phb2024ActorFullById} from "./converters/phb2024-actorFullById.js";
import {phb2024RollTableResultsById} from "./converters/phb2024-rollTableResultsById.js";
import {phb2024ActivitiesById} from "./converters/phb2024-activities-by-id.js";
import {phb2024ActorDetails} from "./converters/phb2024-actor-details.js";

Hooks.once("babele.init", (babele) => {
    if (!babele?.registerConverters) return;

    // Core settings exist at setup, before Babele loads translations at ready.
    Hooks.once("setup", () => {
        const language = game.settings.get("core", "language");
        if (typeof language !== "string" || language.split("-")[0].toLowerCase() !== "es") return;

        babele.registerConverters({
            phb2024ActivitiesById,
            phb2024MergeEffects,
            phb2024AdvancementById,
            phb2024JournalPagesById,
            phb2024JournalEntryFullById,
            phb2024ActorFullById,
            phb2024ActorDetails,
            phb2024RollTableResultsById
        });

        console.log(
            "[Babele - translate-dnd5e-phb-2024-es] Converters registered:",
            Object.keys(babele.converters ?? {})
        );
    });
});
