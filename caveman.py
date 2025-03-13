import bpy
import math
import random

# Limpar cena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Criar um bloco de madeira básico
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, 0))
wood_block = bpy.context.active_object
wood_block.name = "PecaDeMadeira"

# Modificar dimensões para um formato de tábua
wood_block.scale = (2.0, 0.8, 0.2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Adicionar um pouco de variação às bordas
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.02, segments=3)
bpy.ops.object.mode_set(mode='OBJECT')

# Criar material de madeira
wood_material = bpy.data.materials.new(name="MadeiraMaterial")
wood_material.use_nodes = True
nodes = wood_material.node_tree.nodes
links = wood_material.node_tree.links

# Limpar nós padrão
for node in nodes:
    nodes.remove(node)

# Criar nós para o material
output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')
tex_coord = nodes.new(type='ShaderNodeTexCoord')
mapping = nodes.new(type='ShaderNodeMapping')
wood_texture = nodes.new(type='ShaderNodeTexNoise')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
bump = nodes.new(type='ShaderNodeBump')
normal_map = nodes.new(type='ShaderNodeNormalMap')

# Configurar o mapeamento
mapping.inputs['Scale'].default_value[0] = 4.0
mapping.inputs['Scale'].default_value[1] = 20.0
mapping.inputs['Scale'].default_value[2] = 0.5

# Configurar ruído para textura da madeira
wood_texture.inputs['Scale'].default_value = 15.0
wood_texture.inputs['Detail'].default_value = 6.0
wood_texture.inputs['Distortion'].default_value = 0.8

# Configurar ColorRamp para tons de madeira
color_ramp.color_ramp.elements[0].position = 0.3
color_ramp.color_ramp.elements[0].color = (0.05, 0.02, 0.01, 1.0)
color_ramp.color_ramp.elements[1].position = 0.7
color_ramp.color_ramp.elements[1].color = (0.2, 0.1, 0.05, 1.0)

# Adicionar mais elementos ao ColorRamp
element = color_ramp.color_ramp.elements.new(0.5)
element.color = (0.15, 0.07, 0.03, 1.0)

# Configurar bump para superfície
bump.inputs['Strength'].default_value = 0.2
bump.inputs['Distance'].default_value = 0.02

# Configurar o Principled BSDF para aparência polida
principled.inputs['Base Color'].default_value = (0.2, 0.1, 0.05, 1.0)
principled.inputs['Subsurface'].default_value = 0.05
principled.inputs['Metallic'].default_value = 0.0
principled.inputs['Specular'].default_value = 0.5
principled.inputs['Specular Tint'].default_value = 0.0
principled.inputs['Roughness'].default_value = 0.15  # Valor baixo para aparência polida
principled.inputs['Anisotropic'].default_value = 0.7
principled.inputs['Anisotropic Rotation'].default_value = 0.0
principled.inputs['Sheen'].default_value = 0.1
principled.inputs['Clearcoat'].default_value = 0.2
principled.inputs['Clearcoat Roughness'].default_value = 0.1

# Conectar nós
links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], wood_texture.inputs['Vector'])
links.new(wood_texture.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(wood_texture.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], principled.inputs['Normal'])
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Adicionar textura de madeira procedural mais detalhada
texture_coords = nodes.new(type='ShaderNodeTexCoord')
voronoi = nodes.new(type='ShaderNodeTexVoronoi')
mix_rgb = nodes.new(type='ShaderNodeMixRGB')

voronoi.inputs['Scale'].default_value = 20.0
voronoi.inputs['Detail'].default_value = 0.4
voronoi.voronoi_dimensions = '2D'
mix_rgb.blend_type = 'OVERLAY'
mix_rgb.inputs['Fac'].default_value = 0.3

links.new(texture_coords.outputs['Generated'], voronoi.inputs['Vector'])
links.new(voronoi.outputs['Distance'], mix_rgb.inputs[1])
links.new(color_ramp.outputs['Color'], mix_rgb.inputs[2])
links.new(mix_rgb.outputs['Color'], principled.inputs['Base Color'])

# Aplicar material ao objeto
if wood_block.data.materials:
    wood_block.data.materials[0] = wood_material
else:
    wood_block.data.materials.append(wood_material)

# Adicionar subdivisão para suavizar a geometria
subdivision = wood_block.modifiers.new(name="Subdivision", type='SUBSURF')
subdivision.levels = 2
subdivision.render_levels = 3

# Configurar renderização
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 256

# Adicionar uma luz para mostrar o brilho do polimento
bpy.ops.object.light_add(type='AREA', radius=1, location=(2, -2, 3))
light = bpy.context.active_object
light.data.energy = 500
light.data.size = 2.0

# Posicionar a câmera para uma boa visualização
bpy.ops.object.camera_add(location=(3, -3, 1.5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(70), 0, math.radians(45))
bpy.context.scene.camera = camera

print("Objeto de madeira polida criado com sucesso!")
