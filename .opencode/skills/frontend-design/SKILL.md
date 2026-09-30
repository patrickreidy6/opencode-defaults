---
name: frontend-design
description: Design new interfaces or substantive visual redesigns with intentional typography, layout, and interaction.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Use for visual design work, not a behavior-only frontend change or isolated typo. The brief and existing design system set the direction.

## Design direction

- Ground the design in the product, audience, content, and primary action. Infer routine choices from context; clarify a missing product goal if it would change the design substantially.
- For a new visual direction, choose a coherent palette, type hierarchy, spacing system, and layout appropriate to the subject. A distinctive element should serve the brief, not impose novelty on an established interface.
- Use real content where available. Mark invented sample content as illustrative rather than presenting fabricated product claims or metrics as facts.

## Execution

- Make hierarchy and spacing carry the information. Numbering should represent a real sequence; labels and dividers should clarify relationships.
- Choose typography for the content and audience. Reuse existing tokens and components when extending a product.
- Use motion where it explains a transition or reinforces the interaction. Respect reduced-motion preferences and keep keyboard focus visible.
- Treat responsive layouts, readable contrast, and usable controls as part of the implementation.
- Keep CSS specificity predictable so component styles do not silently cancel each other out.

## Interface copy

- Name what the user recognizes and controls: "Notifications," rather than an internal implementation label.
- Use specific action labels and consistent vocabulary through the flow: "Save changes" followed by "Changes saved."
- Give errors and empty states a useful explanation and next action. Keep copy concrete, concise, and appropriate to the product's voice.

## Completion

For implementation requests, continue through the working interface and inspect the rendered result at relevant screen sizes when preview tools are available. Fix issues found in the affected layout and interactions before delivery; state any preview limitation. A concept-only request is complete with the requested design artifact.
