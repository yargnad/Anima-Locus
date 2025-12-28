from fastapi import APIRouter, HTTPException
from typing import List, Dict
from .schemas import Preset, Scene

router = APIRouter()

# In-memory storage for prototype
presets_db: Dict[str, Preset] = {}
scenes_db: Dict[str, Scene] = {}

# --- Presets ---

@router.get("/presets", response_model=List[Preset])
async def list_presets():
    return list(presets_db.values())

@router.post("/presets", response_model=Preset)
async def create_preset(preset: Preset):
    if preset.id in presets_db:
        raise HTTPException(status_code=400, detail="Preset ID already exists")
    presets_db[preset.id] = preset
    return preset

@router.get("/presets/{preset_id}", response_model=Preset)
async def get_preset(preset_id: str):
    if preset_id not in presets_db:
        raise HTTPException(status_code=404, detail="Preset not found")
    return presets_db[preset_id]

# --- Scenes ---

@router.get("/scenes", response_model=List[Scene])
async def list_scenes():
    return list(scenes_db.values())

@router.post("/scenes", response_model=Scene)
async def create_scene(scene: Scene):
    if scene.id in scenes_db:
        raise HTTPException(status_code=400, detail="Scene ID already exists")
    scenes_db[scene.id] = scene
    return scene
