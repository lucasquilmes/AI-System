from pathlib import Path

# General registry to map task names to their configuration
# No schema needed - just raw LLM output
GENERAL_REGISTRY = {
    "classification": {
        "name": "classification",
        "system_prompt": Path("prompts/classification_system.txt"),
        "user_prompt": Path("prompts/classification_user.txt"),
        "output_prefix": "classification",
    },

    "extraction": {
        "name": "extraction",
        "system_prompt": Path("prompts/extraction_system.txt"),
        "user_prompt": Path("prompts/extraction_user.txt"),
        "output_prefix": "extraction",
    },

    "sentiment": {
        "name": "sentiment",
        "system_prompt": Path("prompts/sentiment_system.txt"),
        "user_prompt": Path("prompts/sentiment_user.txt"),
        "output_prefix": "sentiment",
    },

    "custom": {
        "name": "custom",
        "system_prompt": Path("prompts/custom_system.txt"),
        "user_prompt": Path("prompts/custom_user.txt"),
        "output_prefix": "custom",
    },
    # Add other tasks as needed

    "v0": {
        "name": "v0",
        "system_prompt": Path("prompts/v0_system.txt"),
        "user_prompt": Path("prompts/v0_user.txt"),
        "output_prefix": "v0",
    },

    "v1": {
        "name": "v1",
        "system_prompt": Path("prompts/v1_system.txt"),
        "user_prompt": Path("prompts/v1_user.txt"),
        "output_prefix": "v1",
    },

    "v2": {
        "name": "v2",
        "system_prompt": Path("prompts/v2_system.txt"),
        "user_prompt": Path("prompts/v2_user.txt"),
        "output_prefix": "v2",
    },

    "v3": {
        "name": "v3",
        "system_prompt": Path("prompts/v3_system.txt"),
        "user_prompt": Path("prompts/v3_user.txt"),
        "output_prefix": "v3",
    },

    "v4": {
        "name": "v4",
        "system_prompt": Path("prompts/v4_system.txt"),
        "user_prompt": Path("prompts/v4_user.txt"),
        "output_prefix": "v4",
    },

    "v7": {
        "name": "v7",
        "system_prompt": Path("prompts/v7_system.txt"),
        "user_prompt": Path("prompts/v7_user.txt"),
        "output_prefix": "v7",
    },

    "v8": {
        "name": "v8",
        "system_prompt": Path("prompts/v8_system.txt"),
        "user_prompt": Path("prompts/v8_user.txt"),
        "output_prefix": "v8",
    },

    "v5": {
        "name": "v5",
        "system_prompt": Path("prompts/v5_system.txt"),
        "user_prompt": Path("prompts/v5_user.txt"),
        "output_prefix": "v5",
    },

    "v6": {
        "name": "v6",
        "system_prompt": Path("prompts/v6_system.txt"),
        "user_prompt": Path("prompts/v6_user.txt"),
        "output_prefix": "v6",
    },

    "motor": {
        "name": "motor",
        "system_prompt": Path("prompts/motor_system.txt"),
        "user_prompt": Path("prompts/motor_user.txt"),
        "output_prefix": "motor",
    },

    "audit": {
        "name": "audit",
        "system_prompt": Path("prompts/audit_system.txt"),
        "user_prompt": Path("prompts/audit_user.txt"),
        "output_prefix": "audit",
    },

    # --- Técnicas de prompting (Lectura Fácil) ---
    "zero_shot": {
        "name": "zero_shot",
        "system_prompt": Path("prompts/zero_shot_system.txt"),
        "user_prompt": Path("prompts/zero_shot_user.txt"),
        "output_prefix": "zero_shot",
    },
    "few_shot": {
        "name": "few_shot",
        "system_prompt": Path("prompts/few_shot_system.txt"),
        "user_prompt": Path("prompts/few_shot_user.txt"),
        "output_prefix": "few_shot",
    },
    "role": {
        "name": "role",
        "system_prompt": Path("prompts/role_system.txt"),
        "user_prompt": Path("prompts/role_user.txt"),
        "output_prefix": "role",
    },
    "cot": {
        "name": "cot",
        "system_prompt": Path("prompts/cot_system.txt"),
        "user_prompt": Path("prompts/cot_user.txt"),
        "output_prefix": "cot",
    },
    "zs_cot": {
        "name": "zs_cot",
        "system_prompt": Path("prompts/zs_cot_system.txt"),
        "user_prompt": Path("prompts/zs_cot_user.txt"),
        "output_prefix": "zs_cot",
    },
    "tot": {
        "name": "tot",
        "system_prompt": Path("prompts/tot_system.txt"),
        "user_prompt": Path("prompts/tot_user.txt"),
        "output_prefix": "tot",
    },
    "self_cons": {
        "name": "self_cons",
        "system_prompt": Path("prompts/self_cons_system.txt"),
        "user_prompt": Path("prompts/self_cons_user.txt"),
        "output_prefix": "self_cons",
    },
    "self_ref": {
        "name": "self_ref",
        "system_prompt": Path("prompts/self_ref_system.txt"),
        "user_prompt": Path("prompts/self_ref_user.txt"),
        "output_prefix": "self_ref",
    },
    "ensemble": {
        "name": "ensemble",
        "system_prompt": Path("prompts/ensemble_system.txt"),
        "user_prompt": Path("prompts/ensemble_user.txt"),
        "output_prefix": "ensemble",
    },
    "meta": {
        "name": "meta",
        "system_prompt": Path("prompts/meta_system.txt"),
        "user_prompt": Path("prompts/meta_user.txt"),
        "output_prefix": "meta",
    },
}
