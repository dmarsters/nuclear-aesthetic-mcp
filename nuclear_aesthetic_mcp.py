"""
Nuclear Aesthetic MCP Server

A prompt enhancement system for nuclear explosion aesthetics, using the 
temporal-morphological phase coupling as the primary organizational axis.

Architecture follows the three-layer pattern:
- Claude: Interprets creative intent, maps to PhaseForm + modifiers
- MCP: Deterministic taxonomy lookup and parameter mapping
- Output: Structured visual parameters for image generation
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import json
import sys
import asyncio

# Prevent double event loop initialization in FastMCP cloud
_fastmcp_cloud_mode = False
try:
    # Check if we're in FastMCP cloud environment
    loop = asyncio.get_running_loop()
    _fastmcp_cloud_mode = True
except RuntimeError:
    # No loop running, we're in local mode
    pass

# Initialize MCP server
if _fastmcp_cloud_mode:
    # In cloud mode, create server without triggering run()
    import os
    os.environ['MCP_NO_AUTO_RUN'] = '1'

mcp = FastMCP("nuclear_aesthetic_mcp")


# =============================================================================
# ENUMS - Core Taxonomies
# =============================================================================

class PhaseForm(str, Enum):
    """
    Primary axis: Temporal-Morphological coupling.
    Each PhaseForm bundles intrinsic visual properties.
    """
    # Initiation phase (sub-microsecond to microseconds)
    INITIATION_RADIANT_POINT = "initiation.radiant_point"
    INITIATION_THERMAL_BLOOM = "initiation.thermal_bloom"
    
    # Fireball phase (milliseconds to seconds)
    FIREBALL_PLASMA_CORE = "fireball.plasma_core"
    FIREBALL_SURFACE_INSTABILITY = "fireball.surface_instability"
    FIREBALL_EXPANSION_FRONT = "fireball.expansion_front"
    
    # Shock interaction phase (seconds)
    SHOCK_COMPRESSION_DISC = "shock.compression_disc"
    SHOCK_MACH_STEM = "shock.mach_stem"
    SHOCK_WILSON_CLOUD = "shock.wilson_cloud"
    
    # Rise phase (seconds to minutes)
    RISE_VORTEX_STEM = "rise.vortex_stem"
    RISE_TOROIDAL_ROLL = "rise.toroidal_roll"
    RISE_CAULIFLOWER_CAP = "rise.cauliflower_cap"
    
    # Dispersal phase (minutes to hours)
    DISPERSAL_COLUMN_COLLAPSE = "dispersal.column_collapse"
    DISPERSAL_ANVIL_SPREAD = "dispersal.anvil_spread"
    DISPERSAL_FALLOUT_PLUME = "dispersal.fallout_plume"


class Scale(str, Enum):
    """Yield scale - affects rate of evolution and proportions."""
    TACTICAL = "tactical"           # Sub-kiloton: tighter forms, faster evolution
    STRATEGIC = "strategic"         # Kiloton-megaton: canonical imagery
    THERMONUCLEAR = "thermonuclear" # Megaton+: multi-stage, extreme vertical


class Environment(str, Enum):
    """Detonation environment - affects medium interaction."""
    SURFACE = "surface"         # Ground interaction, crater, heavy debris
    AIRBURST = "airburst"       # Clean fireball, minimal ground coupling
    UNDERWATER = "underwater"   # Wilson column, base surge, steam cauliflower
    SPACE = "space"             # No atmosphere, pure plasma expansion
    UNDERGROUND = "underground" # Contained, only venting plumes visible


class Era(str, Enum):
    """Historical era - affects capture aesthetics and color science."""
    TRINITY = "trinity"         # 1945-1950: sepia, high grain, static camera
    PACIFIC = "pacific"         # 1950s: Kodachrome saturation, naval framing
    NEVADA = "nevada"           # 1950s-60s: desert palette, military documentary
    MODERN = "modern"           # CGI/simulation: impossible angles, clean


class Affect(str, Enum):
    """Affective intent - affects framing, emphasis, emotional register."""
    SUBLIME = "sublime"         # Scale, vertical development, luminous extremes
    TERRIBLE = "terrible"       # Shock interaction, destruction vectors
    CLINICAL = "clinical"       # Documentary distance, labeled phases
    MELANCHOLIC = "melancholic" # Dispersal, entropy, fallout
    ANXIOUS = "anxious"         # Anticipation, countdown, moment-before
    SACRED_PROFANE = "sacred_profane"  # Ambivalent awe, beauty-horror tension


# =============================================================================
# INTRINSIC PROPERTIES - What each PhaseForm brings bundled
# =============================================================================

PHASEFORM_INTRINSICS: Dict[str, Dict[str, Any]] = {
    # Initiation phase
    "initiation.radiant_point": {
        "luminous_regime": "thermal_bloom",
        "color_temperature_k": (15000, 50000),
        "luminosity": "extreme_overexposure",
        "form": "point_source_expanding",
        "duration_reference": "sub-microsecond",
        "atmospheric_state": "pre-interaction",
        "key_visual": "pure white point, corona forming",
        "contrast": "infinite_to_environment",
    },
    "initiation.thermal_bloom": {
        "luminous_regime": "thermal_bloom",
        "color_temperature_k": (8000, 15000),
        "luminosity": "total_overexposure",
        "form": "expanding_sphere_undifferentiated",
        "duration_reference": "microseconds",
        "atmospheric_state": "vacuum_formation",
        "key_visual": "white sphere consuming frame, no detail",
        "contrast": "blown_highlights",
    },
    
    # Fireball phase
    "fireball.plasma_core": {
        "luminous_regime": "incandescence",
        "color_temperature_k": (5000, 8000),
        "luminosity": "self_illuminated_bright",
        "form": "sphere_with_internal_structure",
        "duration_reference": "early_milliseconds",
        "atmospheric_state": "plasma_boundary",
        "key_visual": "orange-white sphere, hints of internal convection",
        "contrast": "high_dynamic_range",
    },
    "fireball.surface_instability": {
        "luminous_regime": "incandescence",
        "color_temperature_k": (4000, 6000),
        "luminosity": "self_illuminated",
        "form": "sphere_with_surface_perturbations",
        "duration_reference": "milliseconds",
        "atmospheric_state": "plasma_atmosphere_interface",
        "key_visual": "mottled surface, rope tricks, guy-wire vaporization",
        "contrast": "texture_visible",
    },
    "fireball.expansion_front": {
        "luminous_regime": "incandescence_fading",
        "color_temperature_k": (3000, 5000),
        "luminosity": "bright_but_structured",
        "form": "sphere_cooling_at_edges",
        "duration_reference": "late_milliseconds",
        "atmospheric_state": "shock_detaching",
        "key_visual": "orange core, darker cooling edges, shock separating",
        "contrast": "medium_high",
    },
    
    # Shock interaction phase
    "shock.compression_disc": {
        "luminous_regime": "reflected_flash",
        "color_temperature_k": (5500, 7000),
        "luminosity": "medium_reflected",
        "form": "toroidal_compression_wave",
        "duration_reference": "seconds",
        "atmospheric_state": "compression_haze",
        "key_visual": "visible ring of compressed air, refraction effects",
        "contrast": "subtle_atmospheric",
    },
    "shock.mach_stem": {
        "luminous_regime": "reflected_flash",
        "color_temperature_k": (5000, 6000),
        "luminosity": "ground_reflection",
        "form": "conical_ground_interaction",
        "duration_reference": "seconds",
        "atmospheric_state": "dust_entrainment",
        "key_visual": "dust skirt rising, ground shock visible, debris curtain",
        "contrast": "environmental",
    },
    "shock.wilson_cloud": {
        "luminous_regime": "ambient_reflected",
        "color_temperature_k": (5500, 6500),
        "luminosity": "atmospheric_scatter",
        "form": "condensation_disc_or_dome",
        "duration_reference": "seconds",
        "atmospheric_state": "condensation",
        "key_visual": "white vapor ring/dome, eerie transient cloud",
        "contrast": "soft_ethereal",
    },
    
    # Rise phase
    "rise.vortex_stem": {
        "luminous_regime": "self_illuminated_fading",
        "color_temperature_k": (2500, 4000),
        "luminosity": "internal_glow",
        "form": "columnar_with_internal_vortices",
        "duration_reference": "tens_of_seconds",
        "atmospheric_state": "particulate_dense",
        "key_visual": "rising column, internal fire visible, debris entrainment",
        "contrast": "dramatic_chiaroscuro",
    },
    "rise.toroidal_roll": {
        "luminous_regime": "mixed_internal_ambient",
        "color_temperature_k": (2000, 3500),
        "luminosity": "diminishing_internal",
        "form": "toroidal_vortex_ring",
        "duration_reference": "minute",
        "atmospheric_state": "turbulent_mixing",
        "key_visual": "mushroom cap forming, rolling edges, vortex visible",
        "contrast": "sculptural",
    },
    "rise.cauliflower_cap": {
        "luminous_regime": "ambient_dominant",
        "color_temperature_k": (5500, 6500),
        "luminosity": "externally_lit",
        "form": "fractal_turbulent_mass",
        "duration_reference": "minutes",
        "atmospheric_state": "particulate_cloud",
        "key_visual": "baroque complexity, fractal edges, monumental scale",
        "contrast": "cloud_like",
    },
    
    # Dispersal phase
    "dispersal.column_collapse": {
        "luminous_regime": "ambient",
        "color_temperature_k": (5500, 6500),
        "luminosity": "daylight",
        "form": "collapsing_vertical_structure",
        "duration_reference": "minutes",
        "atmospheric_state": "settling_particulate",
        "key_visual": "stem losing coherence, material falling back",
        "contrast": "naturalistic",
    },
    "dispersal.anvil_spread": {
        "luminous_regime": "ambient",
        "color_temperature_k": (5500, 7000),
        "luminosity": "atmospheric",
        "form": "horizontal_spreading_layer",
        "duration_reference": "tens_of_minutes",
        "atmospheric_state": "stratospheric_injection",
        "key_visual": "cap spreading horizontally, anvil formation",
        "contrast": "high_altitude_clarity",
    },
    "dispersal.fallout_plume": {
        "luminous_regime": "ambient",
        "color_temperature_k": (5000, 6000),
        "luminosity": "hazy",
        "form": "drifting_particulate_mass",
        "duration_reference": "hours",
        "atmospheric_state": "dispersed_contamination",
        "key_visual": "smeared across sky, ominous drift, entropic decay",
        "contrast": "low_atmospheric",
    },
}


# =============================================================================
# MODIFIER EFFECTS - How modifiers transform the base PhaseForm
# =============================================================================

SCALE_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "tactical": {
        "evolution_rate": "fast",
        "vertical_development": "limited",
        "proportions": "compact",
        "detail_scale": "human_reference_visible",
        "color_shift": None,
    },
    "strategic": {
        "evolution_rate": "canonical",
        "vertical_development": "substantial",
        "proportions": "classical_mushroom",
        "detail_scale": "landscape_dwarfing",
        "color_shift": None,
    },
    "thermonuclear": {
        "evolution_rate": "slow_majestic",
        "vertical_development": "extreme",
        "proportions": "towering_multi_stage",
        "detail_scale": "horizon_spanning",
        "color_shift": "secondary_staging_visible",
    },
}

ENVIRONMENT_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "surface": {
        "ground_interaction": "crater_formation",
        "debris_character": "earth_rock_heavy",
        "stem_appearance": "dirty_debris_laden",
        "atmospheric_effect": "dust_dominant",
        "color_influence": "earth_tones_mixed",
    },
    "airburst": {
        "ground_interaction": "minimal_delayed",
        "debris_character": "atmospheric_only",
        "stem_appearance": "clean_plasma",
        "atmospheric_effect": "pure_shock_effects",
        "color_influence": "clean_plasma_colors",
    },
    "underwater": {
        "ground_interaction": "water_column",
        "debris_character": "spray_and_steam",
        "stem_appearance": "wilson_column_dominant",
        "atmospheric_effect": "massive_steam_cauliflower",
        "color_influence": "white_steam_blue_water",
    },
    "space": {
        "ground_interaction": "none",
        "debris_character": "none",
        "stem_appearance": "pure_plasma_sphere_only",
        "atmospheric_effect": "none_pure_expansion",
        "color_influence": "unfiltered_plasma_spectrum",
    },
    "underground": {
        "ground_interaction": "contained_venting",
        "debris_character": "subsidence_crater",
        "stem_appearance": "vent_plumes_only",
        "atmospheric_effect": "localized_dust_jets",
        "color_influence": "earth_tones_dominant",
    },
}

ERA_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "trinity": {
        "color_science": "sepia_monochrome",
        "grain_structure": "heavy_film_grain",
        "camera_characteristics": "static_distant_tripod",
        "frame_quality": "historical_degraded",
        "aspect_ratio": "academic_4x3",
    },
    "pacific": {
        "color_science": "kodachrome_saturated",
        "grain_structure": "medium_film_grain",
        "camera_characteristics": "naval_observation",
        "frame_quality": "military_documentary",
        "aspect_ratio": "widescreen_naval",
    },
    "nevada": {
        "color_science": "desert_warm_tones",
        "grain_structure": "newsreel_grain",
        "camera_characteristics": "bunker_observation",
        "frame_quality": "civil_defense_documentary",
        "aspect_ratio": "television_4x3",
    },
    "modern": {
        "color_science": "digital_clean",
        "grain_structure": "none_or_artificial",
        "camera_characteristics": "impossible_angles",
        "frame_quality": "pristine_cgi",
        "aspect_ratio": "cinematic_wide",
    },
}

AFFECT_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "sublime": {
        "framing": "emphasize_vertical_scale",
        "composition": "human_absence_or_dwarfed",
        "lighting_emphasis": "luminous_extremes",
        "emotional_register": "overwhelming_awe",
        "detail_focus": "totality_over_detail",
    },
    "terrible": {
        "framing": "destruction_vectors_visible",
        "composition": "before_after_implied",
        "lighting_emphasis": "harsh_revealing",
        "emotional_register": "horror_power",
        "detail_focus": "shock_effects_debris",
    },
    "clinical": {
        "framing": "documentary_centered",
        "composition": "measurement_reference",
        "lighting_emphasis": "neutral_informative",
        "emotional_register": "detached_scientific",
        "detail_focus": "phase_identification",
    },
    "melancholic": {
        "framing": "aftermath_emphasis",
        "composition": "entropy_visible",
        "lighting_emphasis": "fading_diffuse",
        "emotional_register": "sorrow_contemplation",
        "detail_focus": "decay_dispersal",
    },
    "anxious": {
        "framing": "anticipation_moment_before",
        "composition": "tension_building",
        "lighting_emphasis": "pre_flash_stillness",
        "emotional_register": "dread_waiting",
        "detail_focus": "countdown_infrastructure",
    },
    "sacred_profane": {
        "framing": "altar_like_monumentality",
        "composition": "beauty_horror_tension",
        "lighting_emphasis": "transcendent_terrible",
        "emotional_register": "ambivalent_awe",
        "detail_focus": "simultaneous_beauty_destruction",
    },
}


# =============================================================================
# INPUT MODELS
# =============================================================================

class EnhanceNuclearAestheticInput(BaseModel):
    """Input for nuclear aesthetic prompt enhancement."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    prompt: str = Field(
        ...,
        description="Base prompt to enhance with nuclear aesthetic parameters",
        min_length=1,
        max_length=2000
    )
    phase_form: PhaseForm = Field(
        ...,
        description="Primary temporal-morphological phase. This is the core selection."
    )
    scale: Optional[Scale] = Field(
        default=Scale.STRATEGIC,
        description="Yield scale: tactical (sub-kt), strategic (kt-Mt), thermonuclear (Mt+)"
    )
    environment: Optional[Environment] = Field(
        default=Environment.AIRBURST,
        description="Detonation environment affecting medium interaction"
    )
    era: Optional[Era] = Field(
        default=None,
        description="Historical era for capture aesthetics. None for neutral/modern."
    )
    affect: Optional[Affect] = Field(
        default=None,
        description="Affective intent for emotional register. None for neutral."
    )


class ListPhaseFormsInput(BaseModel):
    """Input for listing available phase forms."""
    model_config = ConfigDict(extra='forbid')
    
    phase_filter: Optional[str] = Field(
        default=None,
        description="Filter by phase prefix: 'initiation', 'fireball', 'shock', 'rise', 'dispersal'"
    )


class GetPhaseFormDetailsInput(BaseModel):
    """Input for getting detailed phase form information."""
    model_config = ConfigDict(extra='forbid')
    
    phase_form: PhaseForm = Field(
        ...,
        description="The phase form to get details for"
    )


class SuggestPhaseFormInput(BaseModel):
    """Input for suggesting phase form from description."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid'
    )
    
    description: str = Field(
        ...,
        description="Natural language description of desired nuclear aesthetic moment",
        min_length=5,
        max_length=500
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def build_enhancement_output(
    prompt: str,
    phase_form: str,
    intrinsics: Dict[str, Any],
    scale_mods: Dict[str, Any],
    env_mods: Dict[str, Any],
    era_mods: Optional[Dict[str, Any]],
    affect_mods: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Assemble the complete enhancement output structure."""
    
    # Build color temperature guidance
    temp_range = intrinsics.get("color_temperature_k", (5500, 6500))
    
    output = {
        "original_prompt": prompt,
        "phase_form": phase_form,
        "enhanced_prompt_elements": [],
        "visual_parameters": {
            "luminous": {
                "regime": intrinsics.get("luminous_regime"),
                "color_temperature_k": {
                    "min": temp_range[0],
                    "max": temp_range[1]
                },
                "luminosity": intrinsics.get("luminosity"),
                "contrast": intrinsics.get("contrast"),
            },
            "morphological": {
                "form": intrinsics.get("form"),
                "key_visual": intrinsics.get("key_visual"),
            },
            "atmospheric": {
                "state": intrinsics.get("atmospheric_state"),
            },
            "temporal": {
                "duration_reference": intrinsics.get("duration_reference"),
            },
        },
        "modifiers_applied": {
            "scale": scale_mods,
            "environment": env_mods,
        },
    }
    
    if era_mods:
        output["modifiers_applied"]["era"] = era_mods
        output["visual_parameters"]["capture"] = {
            "color_science": era_mods.get("color_science"),
            "grain": era_mods.get("grain_structure"),
            "camera": era_mods.get("camera_characteristics"),
        }
    
    if affect_mods:
        output["modifiers_applied"]["affect"] = affect_mods
        output["visual_parameters"]["composition"] = {
            "framing": affect_mods.get("framing"),
            "emotional_register": affect_mods.get("emotional_register"),
            "detail_focus": affect_mods.get("detail_focus"),
        }
    
    # Build enhanced prompt elements
    elements = [
        f"nuclear explosion, {intrinsics.get('key_visual')}",
        f"{intrinsics.get('luminosity')} lighting",
        f"{intrinsics.get('form')} morphology",
    ]
    
    # Add scale descriptors
    if scale_mods:
        elements.append(f"{scale_mods.get('vertical_development')} vertical development")
        elements.append(f"{scale_mods.get('detail_scale')} scale")
    
    # Add environment descriptors
    if env_mods:
        if env_mods.get("debris_character") != "none":
            elements.append(f"{env_mods.get('debris_character')} debris")
        elements.append(f"{env_mods.get('atmospheric_effect')} atmosphere")
    
    # Add era descriptors
    if era_mods:
        elements.append(f"{era_mods.get('color_science')} color")
        elements.append(f"{era_mods.get('grain_structure')}")
        elements.append(f"{era_mods.get('camera_characteristics')} perspective")
    
    # Add affect descriptors
    if affect_mods:
        elements.append(f"{affect_mods.get('framing')}")
        elements.append(f"{affect_mods.get('emotional_register')} mood")
    
    output["enhanced_prompt_elements"] = elements
    
    # Build synthesized prompt suggestion
    output["synthesized_prompt"] = f"{prompt}, " + ", ".join(elements[:6])
    
    return output


def match_description_to_phaseform(description: str) -> List[Dict[str, Any]]:
    """Match natural language description to likely phase forms."""
    
    description_lower = description.lower()
    matches = []
    
    # Keyword mappings to phase forms with confidence scores
    keyword_mappings = {
        "initiation.radiant_point": {
            "keywords": ["point", "first light", "initial", "origin", "birth", "beginning"],
            "phrases": ["moment of detonation", "first instant", "point source"],
        },
        "initiation.thermal_bloom": {
            "keywords": ["white", "bloom", "overexposed", "blind", "flash", "brilliant"],
            "phrases": ["everything goes white", "pure light", "thermal flash", "blinding"],
        },
        "fireball.plasma_core": {
            "keywords": ["plasma", "core", "sphere", "orange", "hot", "glowing"],
            "phrases": ["ball of fire", "plasma sphere", "incandescent"],
        },
        "fireball.surface_instability": {
            "keywords": ["mottled", "surface", "texture", "rope", "instability", "perturbation"],
            "phrases": ["rope tricks", "surface detail", "mottling"],
        },
        "fireball.expansion_front": {
            "keywords": ["expanding", "growing", "cooling", "edge", "front"],
            "phrases": ["shock separating", "expansion", "cooling edges"],
        },
        "shock.compression_disc": {
            "keywords": ["ring", "disc", "compression", "wave", "shockwave"],
            "phrases": ["compression wave", "visible ring", "shock ring"],
        },
        "shock.mach_stem": {
            "keywords": ["ground", "dust", "debris", "stem", "skirt", "dirt"],
            "phrases": ["dust skirt", "ground interaction", "debris curtain", "mach stem"],
        },
        "shock.wilson_cloud": {
            "keywords": ["cloud", "vapor", "condensation", "wilson", "dome", "eerie"],
            "phrases": ["wilson cloud", "vapor ring", "condensation", "eerie ring"],
        },
        "rise.vortex_stem": {
            "keywords": ["stem", "column", "rising", "vortex", "pillar"],
            "phrases": ["rising column", "stem forming", "vortex stem"],
        },
        "rise.toroidal_roll": {
            "keywords": ["toroid", "roll", "mushroom", "cap", "rolling"],
            "phrases": ["mushroom forming", "rolling edges", "toroidal"],
        },
        "rise.cauliflower_cap": {
            "keywords": ["cauliflower", "baroque", "fractal", "turbulent", "complex", "iconic"],
            "phrases": ["mushroom cloud", "iconic shape", "fractal edges", "baroque complexity"],
        },
        "dispersal.column_collapse": {
            "keywords": ["collapse", "falling", "settling", "decay"],
            "phrases": ["column collapse", "falling back", "losing coherence"],
        },
        "dispersal.anvil_spread": {
            "keywords": ["anvil", "spread", "horizontal", "stratosphere"],
            "phrases": ["spreading out", "anvil cloud", "horizontal spread"],
        },
        "dispersal.fallout_plume": {
            "keywords": ["fallout", "drift", "smear", "aftermath", "contamination", "ominous"],
            "phrases": ["drifting", "fallout", "aftermath", "entropic"],
        },
    }
    
    for phase_form, mapping in keyword_mappings.items():
        score = 0
        matched_terms = []
        
        for keyword in mapping["keywords"]:
            if keyword in description_lower:
                score += 1
                matched_terms.append(keyword)
        
        for phrase in mapping["phrases"]:
            if phrase in description_lower:
                score += 3  # Phrases weighted higher
                matched_terms.append(phrase)
        
        if score > 0:
            matches.append({
                "phase_form": phase_form,
                "confidence_score": score,
                "matched_terms": matched_terms,
                "key_visual": PHASEFORM_INTRINSICS[phase_form]["key_visual"],
            })
    
    # Sort by confidence score descending
    matches.sort(key=lambda x: x["confidence_score"], reverse=True)
    
    return matches[:5]  # Return top 5 matches


# =============================================================================
# MCP TOOLS
# =============================================================================

@mcp.tool(
    name="enhance_nuclear_aesthetic",
    annotations={
        "title": "Enhance Prompt with Nuclear Aesthetic",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def enhance_nuclear_aesthetic(params: EnhanceNuclearAestheticInput) -> str:
    """
    Enhance a prompt with nuclear explosion aesthetic parameters.
    
    Takes a base prompt and phase_form selection, applies deterministic 
    taxonomy lookup to bundle intrinsic visual properties, then layers
    modifier effects from scale, environment, era, and affect.
    
    Returns structured visual parameters and synthesized prompt elements
    suitable for image generation.
    
    Args:
        params (EnhanceNuclearAestheticInput): Enhancement parameters including:
            - prompt (str): Base prompt to enhance
            - phase_form (PhaseForm): Primary temporal-morphological selection
            - scale (Scale): Yield scale modifier
            - environment (Environment): Detonation environment modifier
            - era (Era): Historical capture aesthetics
            - affect (Affect): Emotional register and framing
    
    Returns:
        str: JSON containing visual parameters, modifiers, and synthesized prompt
    """
    
    # Get intrinsic properties for the selected phase form
    phase_key = params.phase_form.value
    intrinsics = PHASEFORM_INTRINSICS.get(phase_key, {})
    
    # Get modifier effects
    scale_mods = SCALE_MODIFIERS.get(params.scale.value if params.scale else "strategic", {})
    env_mods = ENVIRONMENT_MODIFIERS.get(params.environment.value if params.environment else "airburst", {})
    era_mods = ERA_MODIFIERS.get(params.era.value) if params.era else None
    affect_mods = AFFECT_MODIFIERS.get(params.affect.value) if params.affect else None
    
    # Build output
    output = build_enhancement_output(
        prompt=params.prompt,
        phase_form=phase_key,
        intrinsics=intrinsics,
        scale_mods=scale_mods,
        env_mods=env_mods,
        era_mods=era_mods,
        affect_mods=affect_mods
    )
    
    return json.dumps(output, indent=2)


@mcp.tool(
    name="list_phase_forms",
    annotations={
        "title": "List Available Phase Forms",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_phase_forms(params: ListPhaseFormsInput) -> str:
    """
    List all available temporal-morphological phase forms.
    
    Optionally filter by phase prefix (initiation, fireball, shock, rise, dispersal).
    Returns phase form identifiers with their key visual descriptions.
    
    Args:
        params (ListPhaseFormsInput): Optional filter parameters:
            - phase_filter (str): Filter by phase prefix
    
    Returns:
        str: JSON array of phase forms with descriptions
    """
    
    results = []
    
    for phase_form in PhaseForm:
        phase_key = phase_form.value
        
        # Apply filter if specified
        if params.phase_filter:
            if not phase_key.startswith(params.phase_filter.lower()):
                continue
        
        intrinsics = PHASEFORM_INTRINSICS.get(phase_key, {})
        results.append({
            "phase_form": phase_key,
            "key_visual": intrinsics.get("key_visual", ""),
            "duration_reference": intrinsics.get("duration_reference", ""),
            "luminous_regime": intrinsics.get("luminous_regime", ""),
        })
    
    return json.dumps({"phase_forms": results}, indent=2)


@mcp.tool(
    name="get_phase_form_details",
    annotations={
        "title": "Get Phase Form Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_phase_form_details(params: GetPhaseFormDetailsInput) -> str:
    """
    Get complete intrinsic properties for a specific phase form.
    
    Returns all bundled visual parameters that come intrinsically
    with the selected temporal-morphological phase.
    
    Args:
        params (GetPhaseFormDetailsInput): The phase form to inspect:
            - phase_form (PhaseForm): Phase form identifier
    
    Returns:
        str: JSON containing all intrinsic properties
    """
    
    phase_key = params.phase_form.value
    intrinsics = PHASEFORM_INTRINSICS.get(phase_key, {})
    
    output = {
        "phase_form": phase_key,
        "intrinsic_properties": intrinsics,
        "compatible_modifiers": {
            "scales": [s.value for s in Scale],
            "environments": [e.value for e in Environment],
            "eras": [e.value for e in Era],
            "affects": [a.value for a in Affect],
        }
    }
    
    return json.dumps(output, indent=2)


@mcp.tool(
    name="suggest_phase_form",
    annotations={
        "title": "Suggest Phase Form from Description",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def suggest_phase_form(params: SuggestPhaseFormInput) -> str:
    """
    Suggest matching phase forms from a natural language description.
    
    Analyzes the description for keywords and phrases that map to
    specific temporal-morphological phases. Returns ranked suggestions
    with confidence scores.
    
    This is a helper for Claude to map creative intent to taxonomy.
    
    Args:
        params (SuggestPhaseFormInput): Description to analyze:
            - description (str): Natural language description of desired moment
    
    Returns:
        str: JSON array of suggested phase forms with confidence scores
    """
    
    matches = match_description_to_phaseform(params.description)
    
    if not matches:
        return json.dumps({
            "suggestions": [],
            "message": "No strong matches found. Consider browsing phase forms with list_phase_forms."
        }, indent=2)
    
    return json.dumps({
        "description": params.description,
        "suggestions": matches
    }, indent=2)


@mcp.tool(
    name="list_modifiers",
    annotations={
        "title": "List All Modifier Options",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_modifiers() -> str:
    """
    List all available modifier categories and their options.
    
    Returns the complete taxonomy of scale, environment, era, and affect
    modifiers that can be applied to any phase form.
    
    Returns:
        str: JSON containing all modifier categories and options
    """
    
    output = {
        "scale": {
            "description": "Yield scale affecting evolution rate and proportions",
            "options": {k: v for k, v in SCALE_MODIFIERS.items()}
        },
        "environment": {
            "description": "Detonation environment affecting medium interaction",
            "options": {k: v for k, v in ENVIRONMENT_MODIFIERS.items()}
        },
        "era": {
            "description": "Historical era affecting capture aesthetics",
            "options": {k: v for k, v in ERA_MODIFIERS.items()}
        },
        "affect": {
            "description": "Affective intent affecting framing and emotional register",
            "options": {k: v for k, v in AFFECT_MODIFIERS.items()}
        }
    }
    
    return json.dumps(output, indent=2)


