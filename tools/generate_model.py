"""Generate an original low-poly robot for LR4.

Requires: pip install numpy trimesh
Run from the project root: python tools/generate_model.py
Exports a ready-to-use GLB plus a human-inspectable glTF + BIN.
"""
from pathlib import Path
import math
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'models'
OUT.mkdir(exist_ok=True, parents=True)
scene = trimesh.Scene()
count = 0
COLORS = {
    'shell':  '#E7EDF7',
    'shell_shadow': '#AFBED0',
    'dark':   '#142335',
    'dark2':  '#233B51',
    'cyan':   '#53E1E5',
    'sky':    '#2FAAC9',
    'gold':   '#FFBB63',
    'orange': '#FF795C',
    'chrome': '#728BA4',
    'ice':    '#B6F7FF',
}

def rgba(color):
    return [int(color[i:i+2],16) for i in (1,3,5)] + [255]

def add(mesh, name, col, metallic=0.15, roughness=0.45, emissive=None):
    global count
    opts = dict(name=name, baseColorFactor=rgba(COLORS[col]), metallicFactor=metallic, roughnessFactor=roughness, alphaMode='OPAQUE', doubleSided=False)
    if emissive:
        opts['emissiveFactor'] = [int(COLORS[col][i:i+2],16)/255*emissive for i in (1,3,5)]
    mesh.visual = TextureVisuals(material=PBRMaterial(**opts))
    scene.add_geometry(mesh, node_name=f'{name}_{count:02d}', geom_name=f'{name}_{count:02d}')
    count += 1

def box(name, center, size, color, **kw):
    mesh=trimesh.creation.box(extents=size)
    mesh.apply_translation(center)
    add(mesh,name,color,**kw)

def ellipsoid(name, center, scale, color, subdivision=2, **kw):
    mesh=trimesh.creation.icosphere(subdivisions=subdivision, radius=1)
    mesh.apply_scale(scale)
    mesh.apply_translation(center)
    add(mesh,name,color,**kw)

def cyl(name, center, radius, height, color, direction='y', sections=16, **kw):
    mesh=trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    if direction=='y':
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
    elif direction=='x':
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
    mesh.apply_translation(center)
    add(mesh,name,color,**kw)

def beam(name, start, end, radius, color, sections=12, **kw):
    a=np.array(start,dtype=float); b=np.array(end,dtype=float)
    mid=(a+b)/2
    mesh=trimesh.creation.cylinder(radius=radius,height=float(np.linalg.norm(b-a)), sections=sections)
    transform=trimesh.geometry.align_vectors([0,0,1], b-a)
    mesh.apply_transform(transform)
    mesh.apply_translation(mid)
    add(mesh,name,color,**kw)

# Sturdy legs and oversized cartoon robot boots (front is +Z).
for sign,label in [(-1,'L'),(1,'R')]:
    x=sign*0.145
    box(f'leg_{label}', (x,0.205,-0.008), (0.118,0.22,0.13), 'chrome', metallic=0.6)
    ellipsoid(f'boot_{label}', (x,0.088,0.07), (0.139,0.091,0.175), 'dark', subdivision=2)
    box(f'boot_toecap_{label}', (x,0.068,0.165), (0.16,0.065,0.060), 'cyan',metallic=.2)

# Rounded pear-shaped upper shell and backpack.
ellipsoid('torso', (0,0.455,0), (0.251,0.300,0.184), 'shell', subdivision=2, metallic=.24)
box('backpack', (0,0.47,-0.21), (0.33,0.36,0.10), 'dark2',metallic=.5)
box('belt', (0,0.312,0.103), (0.38,0.083,0.15),'dark2')
box('chest_panel', (0,0.483,0.174), (0.32,0.240,0.052),'sky',metallic=.28)
box('chest_panel_highlight',(0,0.556,0.203),(0.27,0.036,0.014),'ice', emissive=.24)
cyl('core_ring',(0,0.45,0.214),.078,.018,'dark2',direction='z',metallic=.7)
cyl('core_glow',(0,0.45,0.228),.051,.019,'cyan',direction='z',metallic=.05,emissive=.62)
cyl('core_dot',(0,0.45,0.242),.018,.020,'shell',direction='z',emissive=.3)
for x in (-.126,.126):
    box('vent',(x,.365,.205),(.040,.018,.017),'gold',metallic=.35)

# Rounded head, contrasting face shield and illuminated eyes.
ellipsoid('head', (0,0.839,0.006), (.309,.235,.238), 'shell',subdivision=2,metallic=.20)
ellipsoid('head_back',(0,.839,-.122),(.266,.188,.140),'shell_shadow',subdivision=2,metallic=.25)
ellipsoid('visor',(0,0.845,.196),(.249,.132,.072),'dark',subdivision=2,metallic=.35,roughness=.25)
for sign,label in [(-1,'L'),(1,'R')]:
    x=sign*.105
    ellipsoid(f'eye_{label}',(x,.852,.258),(.047,.054,.012),'cyan',subdivision=2,emissive=.85,roughness=.12)
    ellipsoid(f'eye_glint_{label}',(x-.012,.869,.272),(.011,.016,.006),'shell',subdivision=1,emissive=.8)
    cyl(f'ear_{label}',(sign*.316,.835,-.006),.100,.048,'sky',direction='x',metallic=.4)
    cyl(f'ear_cap_{label}',(sign*.343,.835,-.006),.063,.015,'dark2',direction='x',metallic=.65)

# Symmetric jointed arms, one arm tilted upwards as a friendly greeting.
for sign,label in [(-1,'L'),(1,'R')]:
    shoulder=(sign*.260,.620,0)
    elbow=(sign*.381,.445,.018) if sign<0 else (sign*.395,.595,.018)
    wrist=(sign*.433,.320,.048) if sign<0 else (sign*.480,.706,.042)
    ellipsoid(f'shoulder_{label}',shoulder,(.101,.099,.095),'sky',subdivision=2,metallic=.25)
    beam(f'upper_arm_{label}',shoulder,elbow,.066,'chrome',metallic=.45)
    ellipsoid(f'elbow_{label}',elbow,(.071,.074,.075),'dark2',subdivision=1)
    beam(f'forearm_{label}',elbow,wrist,.066,'shell_shadow',metallic=.35)
    ellipsoid(f'hand_{label}',wrist,(.094,.094,.095),'dark',subdivision=2,metallic=.22)
    ellipsoid(f'hand_accent_{label}',(wrist[0],wrist[1]+.013,wrist[2]+.075),(.055,.046,.024),'cyan',subdivision=1,emissive=.16)

# Antenna and warm signal light.
cyl('antenna_base',(0,1.060,-.008),.062,.06,'dark2', metallic=.35)
cyl('antenna',(0,1.150,-.008),.020,.16,'chrome',metallic=.7)
ellipsoid('antenna_tip',(0,1.250,-.008),(.066,.066,.066),'gold',subdivision=2,emissive=.32)

# Two small jet nozzles, visible when the model rotates.
for x in (-.105,.105):
    cyl('jet_nozzle',(x,.430,-.294),.063,.085,'chrome',direction='z',metallic=.6)
    cyl('jet_inside',(x,.430,-.345),.037,.01,'orange',direction='z',emissive=.45)

# Export both formats, using the same geometry and PBR materials.
glb_path=OUT/'astrabot.glb'
glb_path.write_bytes(trimesh.exchange.gltf.export_glb(scene))
files=trimesh.exchange.gltf.export_gltf(scene, merge_buffers=True)
# Fix the exported .gltf name and its external .bin filename through paths only.
for filename, payload in files.items():
    dst = OUT / ('astrabot.gltf' if filename.endswith('.gltf') else filename)
    dst.write_bytes(payload)
print('Meshes:',count)
for p in sorted(OUT.iterdir()): print(p.name, p.stat().st_size)
print('Bounds (meters):',scene.bounds.tolist())
