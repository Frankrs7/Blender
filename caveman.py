import bpy
import math

# Limpar cena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Criar a base da clava (cilindro)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=8,
    radius=0.04,
    depth=0.8,
    enter_editmode=False,
    location=(0, 0, 0)
)
cabo = bpy.context.active_object
cabo.name = "Cabo_Clava"

# Entrar no modo de edição e selecionar os vértices superiores para alargá-los
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

# Selecionar os vértices superiores
for v in cabo.data.vertices:
    if v.co.z > 0.3:
        v.select = True

# Retornar ao modo de edição e escalar os vértices selecionados
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.transform.resize(value=(1.5, 1.5, 1.0))
bpy.ops.object.mode_set(mode='OBJECT')

# Adicionar a cabeça da clava (icosfera)
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=1,
    radius=0.15,
    enter_editmode=False,
    location=(0, 0, 0.5)
)
cabeca = bpy.context.active_object
cabeca.name = "Cabeca_Clava"

# Deformar a cabeça para parecer mais irregular
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.transform.resize(value=(1.2, 1.0, 1.3))
bpy.ops.object.mode_set(mode='OBJECT')

# Adicionar algumas protuberâncias à cabeça da clava
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

# Selecionar alguns vértices aleatórios para criar protuberâncias
vertices_para_protuberancia = [1, 3, 5, 7, 9]
for i in vertices_para_protuberancia:
    if i < len(cabeca.data.vertices):
        cabeca.data.vertices[i].select = True

# Extrudir vértices selecionados
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate=(0, 0, 0.04)
)
bpy.ops.object.mode_set(mode='OBJECT')

# Juntar os objetos em um único
bpy.ops.object.select_all(action='DESELECT')
cabeca.select_set(True)
cabo.select_set(True)
bpy.context.view_layer.objects.active = cabo
bpy.ops.object.join()
clava = bpy.context.active_object
clava.name = "Clava_Prehistorica"

# Adicionar um modificador subdivision para suavizar levemente
modifier = clava.modifiers.new(name="Subdivisão", type='SUBSURF')
modifier.levels = 1
modifier.render_levels = 1

# Criar materiais
# Material para o cabo
material_cabo = bpy.data.materials.new(name="Material_Cabo")
material_cabo.use_nodes = True
nodes_cabo = material_cabo.node_tree.nodes
bsdf_cabo = nodes_cabo.get("Principled BSDF")
if bsdf_cabo:
    bsdf_cabo.inputs["Base Color"].default_value = (0.35, 0.2, 0.05, 1.0)  # Marrom
    bsdf_cabo.inputs["Roughness"].default_value = 0.9
    bsdf_cabo.inputs["Specular"].default_value = 0.1

# Material para a cabeça
material_cabeca = bpy.data.materials.new(name="Material_Cabeca")
material_cabeca.use_nodes = True
nodes_cabeca = material_cabeca.node_tree.nodes
bsdf_cabeca = nodes_cabeca.get("Principled BSDF")
if bsdf_cabeca:
    bsdf_cabeca.inputs["Base Color"].default_value = (0.3, 0.3, 0.3, 1.0)  # Cinza escuro
    bsdf_cabeca.inputs["Roughness"].default_value = 0.8
    bsdf_cabeca.inputs["Specular"].default_value = 0.2

# Atribuir materiais às partes correspondentes
# Primeiro, limpar materiais existentes
while len(clava.data.materials) > 0:
    clava.data.materials.pop(index=0)

# Adicionar os novos materiais
clava.data.materials.append(material_cabo)
clava.data.materials.append(material_cabeca)

# Selecionar faces para aplicar materiais
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

# Aplicar material do cabo (material_index=0)
for face in clava.data.polygons:
    # As faces do cabo estão na parte inferior
    if face.center.z < 0.35:
        face.material_index = 0
    else:
        face.material_index = 1

# Adicionar textura procedural
# Criar textura de madeira para o cabo
texture_nodes = material_cabo.node_tree.nodes
texture_links = material_cabo.node_tree.links

noise_texture = texture_nodes.new('ShaderNodeTexNoise')
noise_texture.inputs["Scale"].default_value = 15.0
noise_texture.inputs["Detail"].default_value = 3.0

color_ramp = texture_nodes.new('ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].position = 0.3
color_ramp.color_ramp.elements[0].color = (0.25, 0.15, 0.05, 1.0)
color_ramp.color_ramp.elements[1].position = 0.7
color_ramp.color_ramp.elements[1].color = (0.35, 0.2, 0.05, 1.0)

texture_links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
texture_links.new(color_ramp.outputs["Color"], bsdf_cabo.inputs["Base Color"])

# Criar textura rochosa para a cabeça
texture_nodes_cabeca = material_cabeca.node_tree.nodes
texture_links_cabeca = material_cabeca.node_tree.links

voronoi_texture = texture_nodes_cabeca.new('ShaderNodeTexVoronoi')
voronoi_texture.inputs["Scale"].default_value = 30.0

bump_node = texture_nodes_cabeca.new('ShaderNodeBump')
bump_node.inputs["Strength"].default_value = 0.3

texture_links_cabeca.new(voronoi_texture.outputs["Distance"], bump_node.inputs["Height"])
texture_links_cabeca.new(bump_node.outputs["Normal"], bsdf_cabeca.inputs["Normal"])

# RIG (Armature) para animar a clava
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, -0.4))
armature = bpy.context.active_object
armature.name = "Armature_Clava"

# Configurar ossos
bone = armature.data.edit_bones[0]
bone.name = "Bone_Handle"
bone.tail = (0, 0, 0.3)

# Adicionar um segundo osso para a cabeça
head_bone = armature.data.edit_bones.new("Bone_Head")
head_bone.head = (0, 0, 0.3)
head_bone.tail = (0, 0, 0.7)
head_bone.parent = bone

# Finalizar a edição da armature
bpy.ops.object.mode_set(mode='OBJECT')

# Parenting da clava com a armature
bpy.ops.object.select_all(action='DESELECT')
clava.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Configurar a Clava como objeto ativo e centralizar na cena
bpy.ops.object.select_all(action='DESELECT')
clava.select_set(True)
bpy.context.view_layer.objects.active = clava

# Configurar visualização do viewport para ver melhor o modelo
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

print("Clava pré-histórica criada com sucesso!")
