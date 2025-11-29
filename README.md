# Nuclear Aesthetic MCP Server

A prompt enhancement system for nuclear explosion aesthetics, implementing a categorical olog architecture with the **temporal-morphological phase coupling** as the primary organizational axis.

## Architecture

This MCP follows the three-layer pattern for cost-effective prompt enhancement:

1. **Claude Layer**: Interprets creative intent, maps natural language descriptions to PhaseForm + modifiers
2. **MCP Layer**: Deterministic taxonomy lookup and parameter mapping (no LLM inference)
3. **Output Layer**: Structured visual parameters ready for image generation

### Why This Architecture?

The temporal-morphological coupling eliminates redundant parameter specification. Each PhaseForm bundles its intrinsic visual properties—you don't specify "thermal bloom" lighting separately because `initiation.thermal_bloom` *is* the thermal bloom lighting. The coupling means:

- Cleaner API surface
- Fewer parameters to get wrong
- Visual coherence guaranteed by the taxonomy

## Core Concepts

### PhaseForm (Primary Axis)

The fusion of temporal phase and morphological form:

```
Initiation Phase (sub-μs to μs)
├── initiation.radiant_point      → pure white point, corona forming
└── initiation.thermal_bloom      → white sphere consuming frame

Fireball Phase (ms to seconds)
├── fireball.plasma_core          → orange-white sphere, internal convection
├── fireball.surface_instability  → mottled surface, rope tricks
└── fireball.expansion_front      → cooling edges, shock separating

Shock Phase (seconds)
├── shock.compression_disc        → visible ring of compressed air
├── shock.mach_stem              → dust skirt, debris curtain
└── shock.wilson_cloud           → white vapor ring, eerie transient

Rise Phase (seconds to minutes)
├── rise.vortex_stem             → rising column, internal fire
├── rise.toroidal_roll           → mushroom cap forming, rolling edges
└── rise.cauliflower_cap         → baroque complexity, fractal edges

Dispersal Phase (minutes to hours)
├── dispersal.column_collapse    → stem losing coherence
├── dispersal.anvil_spread       → cap spreading horizontally
└── dispersal.fallout_plume      → drifting, ominous, entropic
```

### Modifiers (Secondary Axes)

Modifiers transform the base PhaseForm without changing its identity:

**Scale** (yield)
- `tactical` — sub-kiloton, tight forms, fast evolution
- `strategic` — kiloton-megaton, canonical imagery
- `thermonuclear` — megaton+, multi-stage, extreme vertical

**Environment** (medium interaction)
- `surface` — crater, earth debris, dirty stem
- `airburst` — clean fireball, pure shock effects
- `underwater` — Wilson column, massive steam
- `space` — no atmosphere, pure plasma expansion
- `underground` — contained, vent plumes only

**Era** (capture aesthetics)
- `trinity` — sepia, heavy grain, static camera
- `pacific` — Kodachrome, naval framing
- `nevada` — desert palette, civil defense documentary
- `modern` — CGI clean, impossible angles

**Affect** (emotional register)
- `sublime` — overwhelming scale, luminous extremes
- `terrible` — destruction vectors, horror/power
- `clinical` — documentary, measurement reference
- `melancholic` — aftermath, entropy, sorrow
- `anxious` — anticipation, countdown, dread
- `sacred_profane` — beauty-horror tension

## Tools

### `enhance_nuclear_aesthetic`

Main enhancement tool. Takes a prompt + PhaseForm + modifiers, returns structured parameters.

```python
# Example invocation
{
    "prompt": "explosion over desert landscape",
    "phase_form": "rise.cauliflower_cap",
    "scale": "thermonuclear",
    "environment": "airburst",
    "era": "nevada",
    "affect": "sublime"
}
```

Returns:
- `visual_parameters`: color temperature, luminosity, contrast, form, atmosphere
- `modifiers_applied`: all active modifier effects
- `enhanced_prompt_elements`: array of descriptive elements
- `synthesized_prompt`: ready-to-use enhanced prompt

### `suggest_phase_form`

Maps natural language to PhaseForm suggestions. Claude uses this to interpret creative intent.

```python
{"description": "that moment where everything goes white but you can still see shape forming"}
# Returns: initiation.thermal_bloom with high confidence
```

### `list_phase_forms`

Browse available phase forms, optionally filtered by phase prefix.

```python
{"phase_filter": "fireball"}
# Returns: plasma_core, surface_instability, expansion_front
```

### `get_phase_form_details`

Inspect complete intrinsic properties for a specific PhaseForm.

### `list_modifiers`

Browse all modifier categories and their effects.

## Usage Pattern

**Claude's workflow:**

1. Receive user's creative intent (natural language)
2. Call `suggest_phase_form` to map intent → PhaseForm candidates
3. Select best PhaseForm, determine appropriate modifiers
4. Call `enhance_nuclear_aesthetic` with selections
5. Use returned parameters to guide image generation prompt

**Example conversation:**

User: "I want that eerie moment with the vapor ring"

Claude interprets → calls `suggest_phase_form`:
```json
{"description": "eerie moment with vapor ring"}
```

MCP returns `shock.wilson_cloud` as top match.

Claude calls `enhance_nuclear_aesthetic`:
```json
{
    "prompt": "nuclear test atmospheric phenomenon",
    "phase_form": "shock.wilson_cloud",
    "scale": "strategic",
    "environment": "airburst",
    "affect": "sublime"
}
```

Gets structured parameters for image generation.

## Installation

```bash
cd nuclear_aesthetic_mcp
pip install -e .
```

## Running

```bash
# stdio transport (local)
python nuclear_aesthetic_mcp.py

# Or via installed script
nuclear-aesthetic-mcp
```

## Integration with Claude

Add to your MCP configuration:

```json
{
    "mcpServers": {
        "nuclear_aesthetic": {
            "command": "python",
            "args": ["/path/to/nuclear_aesthetic_mcp.py"]
        }
    }
}
```

## Categorical Structure

The olog underlying this system:

```
Objects:
- PhaseForm (primary, bundled temporal-morphological states)
- Scale, Environment, Era, Affect (modifier categories)
- VisualParameters (output space)

Morphisms:
- enhance: PhaseForm × Scale × Environment × Era? × Affect? → VisualParameters
- suggest: Description → List[PhaseForm × Confidence]

Commutative Properties:
- Modifier application is commutative (order doesn't matter)
- PhaseForm intrinsics override conflicting modifier suggestions
```

The key insight: temporal phase and morphological form are not independent axes. A "Wilson cloud" only exists during the shock phase. A "cauliflower cap" only exists during the rise phase. The coupling is *physical*, so the taxonomy reflects it.

## License
MIT

## Author
Dal Marsters
