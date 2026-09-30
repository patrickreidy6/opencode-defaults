# Blender Beginner Workspace

## Purpose
- This folder is for learning Blender with help from GPT through OpenCode.
- Explain unfamiliar terms briefly and give concrete, beginner-friendly steps.
- Build the requested model in small, visible stages that are easy to inspect.
- Use the installed Blender application and its Python API (`bpy`).
- The MCP integration is the third-party `ahujasid/mcp-for-blender` project.

## Project Files
- Copy this preset's `AGENTS.md` and `opencode.json` into a dedicated Blender workspace; keep this guide at its root.
- Save Blender scenes here with descriptive names, such as `wooden_table_v01.blend`.
- Create `scripts/` only when reusable Python modeling scripts are needed.
- Create `renders/` when saving images, and `assets/` when adding textures or references.
- Use `exports/` for delivery formats such as `.glb`, `.fbx`, or `.stl`.
- Prefer relative asset paths so scenes remain portable.
- Keep names simple: lowercase words separated by underscores.
- The OpenCode MCP connection is configured in the adjacent `opencode.json`. The preset requires `uvx` on PATH and the installed Blender add-on.

## Starting a Session
1. Open Blender and load the scene you want to work on.
2. In the 3D viewport, press `N` to show the right-hand sidebar.
3. In **MCP for Blender**, check for **Connected on port 9876**, or click **Connect to MCP server**.
4. If the tab is absent, enable the add-on in **Edit > Preferences > Add-ons**.
5. Start OpenCode from the dedicated Blender workspace.
6. After OpenCode configuration changes, quit and restart OpenCode.
7. Ask the agent to inspect the scene before requesting changes.
8. Keep Blender open while using the MCP tools.

## First Checks for the Agent
- Call `get_addon_status` to check the Blender version and add-on compatibility.
- Call `get_scene_info` to see the existing objects before making edits.
- Use `get_viewport_screenshot` to understand the current view.
- Check the active object, selection, mode, dimensions, and scene units.
- State a short plan using plain language before a substantial modeling change.
- Ask about dimensions or intended use only when they materially affect the result.
- Treat existing objects and materials as user work; preserve them unless asked.

## A Simple Modeling Workflow
1. Pick one object, such as a cup, table, planter, or low-poly house.
2. Establish its approximate dimensions and overall silhouette first.
3. Block it out with cubes, cylinders, spheres, or simple meshes.
4. Check proportions from the front, side, and perspective views.
5. Add details in small batches, inspecting after each meaningful change.
6. Add materials once the shape is working.
7. Set up a camera and simple lighting for a preview.
8. Save the `.blend` scene, inspect the preview, then refine or export.

## Beginner Vocabulary
- **Object:** an item in the scene, such as a mesh, camera, or light.
- **Mesh:** geometry made of vertices (points), edges (lines), and faces (surfaces).
- **Object Mode:** move, rotate, and scale whole objects.
- **Edit Mode:** change the vertices, edges, and faces inside a mesh.
- **Modifier:** an adjustable operation, such as beveling edges or adding symmetry.
- **Material:** settings controlling a surface's color and light response.
- **Collection:** a group used to organize scene objects.
- **Render:** an image calculated from the scene's camera, lights, and materials.

## Useful Default Shortcuts
- Middle-mouse drag orbits; Shift + middle-mouse drag pans; the wheel zooms.
- `G`, `R`, and `S` move, rotate, and scale the selection.
- Follow a transform with `X`, `Y`, or `Z` to constrain its axis.
- Type a number during a transform for a precise value; Enter confirms.
- `Tab` switches between Object Mode and Edit Mode for meshes.
- `Shift + A` opens the Add menu; `F3` searches for commands.
- Numpad `1`, `3`, and `7` show front, right, and top views.
- Numpad `.` frames the selection; use **View > Frame Selected** without a numpad.
- `Ctrl + S` saves; `F12` renders the active camera; `Esc` cancels an operation.

## Python and MCP Practices
- Run `bpy` code inside Blender, not the repository's normal Python interpreter.
- Use `execute_blender_code` for short, focused modeling operations.
- Use `bpy_api_lookup` or version-matched documentation for uncertain API calls.
- Use `describe_node_type` before assuming shader or geometry-node socket names.
- Prefer named object references over assumptions about the current selection.
- Set the required mode and active object explicitly when using `bpy.ops`.
- Find shader nodes by type; display names can change with Blender's language.
- Set render colors on material shader inputs, not just viewport display colors.
- Give new objects, collections, and materials meaningful names.
- Avoid duplicate objects when repeating a script; update the intended objects.
- Keep modifiers editable until applying them is necessary for the requested result.
- Explain a failed operation, inspect the cause, and retry only the affected step.

## Checking and Saving Work
- After meaningful edits, inspect both scene information and a viewport screenshot.
- Check dimensions, object placement, shading, and the camera view.
- Start with small preview renders before increasing resolution or render samples.
- Save numbered checkpoints before large changes, such as `wooden_table_v02.blend`.
- Keep the editable `.blend` scene even when delivering an exported model.
- Report the saved file path and what was visually checked.

## Connection Troubleshooting
- Run `opencode mcp list` from the repository root to check the MCP server status.
- A connected MCP process still needs Blender's sidebar server to be running.
- This connection uses `127.0.0.1:9876`, safe mode, and disabled telemetry.
- The add-on auto-connects on startup; if disconnected, reconnect in the sidebar.
- For timeouts, test scene inspection first and split large modeling operations into smaller steps.

## References
- Blender manual: https://docs.blender.org/manual/en/latest/
- Python API: https://docs.blender.org/api/current/ (choose the installed Blender version).
- MCP setup and updates: https://github.com/ahujasid/mcp-for-blender
