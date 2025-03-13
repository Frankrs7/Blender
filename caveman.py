import bpy
import bmesh
import math
import random

# Limpar cena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Função para criar o cabo de madeira
def criar_cabo():
    # Criar um cilindro para o cabo
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=0.03,
        depth=0.8,
        enter_editmode=False,
        location=(0, 0, 0),
        rotation=(0, math.radians(90), 0)
    )
    cabo = bpy.context.active_object
    cabo.name = "Cabo_Machado"
    
    # Adicionar uma leve curvatura ao cabo
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Selecionar os vértices do meio para dobrar levemente
    for v in cabo.data.vertices:
        if -0.2 < v.co.x < 0.2:
            v.select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.translate(value=(0, 0.03, 0))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Afinar a parte traseira do cabo
    for v in cabo.data.vertices:
        if v.co.x < -0.3:
            v.select = True
        else:
            v.select = False
            
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.0, 0.7, 0.7))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return cabo

# Função para criar a cabeça de pedra do machado
def criar_cabeca_machado():
    # Criar a pedra principal usando um cubo deformado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        location=(0.35, 0, 0)
    )
    cabeca = bpy.context.active_object
    cabeca.name = "Cabeca_Machado"
    
    # Dimensionar para forma básica de machado
    bpy.ops.transform.resize(value=(0.15, 0.1, 0.2))
    
    # Modificar o formato para parecer uma pedra talhada irregular
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(cabeca.data)
    
    # Subdividir para criar mais vértices para manipulação
    for f in bm.faces:
        f.select = True
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Atualizar o bmesh
    bmesh.update_edit_mesh(cabeca.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Deformar os vértices aleatoriamente para criar irregularidade
    for v in cabeca.data.vertices:
        # Manter o furo central mais regular
        distance_from_center = ((v.co.x - 0.35)**2 + v.co.y**2)**0.5
        if distance_from_center > 0.05:  # Se não estiver na área do orifício para o cabo
            v.co.x += random.uniform(-0.01, 0.01)
            v.co.y += random.uniform(-0.01, 0.01)
            v.co.z += random.uniform(-0.01, 0.01)
    
    # Criar o ponto afiado (a lâmina)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Selecionar os vértices da frente para formar a lâmina
    for v in cabeca.data.vertices:
        if v.co.x > 0.45:
            v.select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.3, 0.6, 0.7))
    bpy.ops.transform.translate(value=(0.05, 0, 0))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Criar o orifício para o cabo
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=0.032,
        depth=0.3,
        enter_editmode=False,
        location=(0.35, 0, 0),
        rotation=(0, math.radians(90), 0)
    )
    cilindro_booleano = bpy.context.active_object
    cilindro_booleano.name = "Cilindro_Booleano"
    cilindro_booleano.display_type = 'WIRE'
    
    # Configurar o modificador booleano
    cabeca.modifiers["Boolean"].object = cilindro_booleano
    cabeca.modifiers["Boolean"].operation = 'DIFFERENCE'
    
    # Aplicar o modificador booleano
    bpy.context.view_layer.objects.active = cabeca
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    # Excluir o cilindro booleano
    bpy.ops.object.select_all(action='DESELECT')
    cilindro_booleano.select_set(True)
    bpy.ops.object.delete()
    
    return cabeca

# Função para criar cordas que amarram a pedra ao cabo
def criar_cordas(cabo, cabeca):
    # Criar o primeiro anel de corda
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.05,
        minor_radius=0.008,
        major_segments=12,
        minor_segments=6,
        location=(0.32, 0, 0),
        rotation=(0, math.radians(90), 0)
    )
    corda1 = bpy.context.active_object
    corda1.name = "Corda1_Machado"
    
    # Criar o segundo anel de corda
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.05,
        minor_radius=0.008,
        major_segments=12,
        minor_segments=6,
        location=(0.38, 0, 0),
        rotation=(0, math.radians(90), 0)
    )
    corda2 = bpy.context.active_object
    corda2.name = "Corda2_Machado"
    
    # Achatar os anéis e deformar levemente para parecer corda amarrada
    for corda in [corda1, corda2]:
        bpy.context.view_layer.objects.active = corda
        bpy.ops.transform.resize(value=(1.0, 1.0, 0.5))
        
        # Deformar aleatoriamente para parecer menos perfeito
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.vertex_random(offset=0.003)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    return [corda1, corda2]

# Criar materiais
def criar_materiais():
    # Material para o cabo (madeira)
    material_cabo = bpy.data.materials.new(name="Material_Cabo")
    material_cabo.use_nodes = True
    nodes_cabo = material_cabo.node_tree.nodes
    links_cabo = material_cabo.node_tree.links
    
    # Limpar os nós existentes
    for node in nodes_cabo:
        nodes_cabo.remove(node)
    
    # Adicionar Principled BSDF
    bsdf_cabo = nodes_cabo.new('ShaderNodeBsdfPrincipled')
    bsdf_cabo.location = (0, 0)
    bsdf_cabo.inputs["Base Color"].default_value = (0.35, 0.2, 0.05, 1.0)  # Marrom
    bsdf_cabo.inputs["Roughness"].default_value = 0.8
    bsdf_cabo.inputs["Specular"].default_value = 0.1
    
    # Adicionar textura de ruído para a madeira
    noise_tex = nodes_cabo.new('ShaderNodeTexNoise')
    noise_tex.location = (-300, 0)
    noise_tex.inputs["Scale"].default_value = 50.0
    noise_tex.inputs["Detail"].default_value = 6.0
    noise_tex.inputs["Distortion"].default_value = 0.5
    
    # Ramp de cores para a madeira
    color_ramp = nodes_cabo.new('ShaderNodeValToRGB')
    color_ramp.location = (-150, 0)
    color_ramp.color_ramp.elements[0].position = 0.4
    color_ramp.color_ramp.elements[0].color = (0.25, 0.15, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (0.35, 0.2, 0.05, 1.0)
    
    # Mapeamento de textura
    tex_coord = nodes_cabo.new('ShaderNodeTexCoord')
    tex_coord.location = (-500, 0)
    mapping = nodes_cabo.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    
    # Saída do material
    output = nodes_cabo.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Conexões
    links_cabo.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links_cabo.new(mapping.outputs["Vector"], noise_tex.inputs["Vector"])
    links_cabo.new(noise_tex.outputs["Fac"], color_ramp.inputs["Fac"])
    links_cabo.new(color_ramp.outputs["Color"], bsdf_cabo.inputs["Base Color"])
    links_cabo.new(bsdf_cabo.outputs["BSDF"], output.inputs["Surface"])
    
    # Material para a cabeça de pedra
    material_cabeca = bpy.data.materials.new(name="Material_Pedra")
    material_cabeca.use_nodes = True
    nodes_cabeca = material_cabeca.node_tree.nodes
    links_cabeca = material_cabeca.node_tree.links
    
    # Limpar os nós existentes
    for node in nodes_cabeca:
        nodes_cabeca.remove(node)
    
    # Adicionar Principled BSDF
    bsdf_cabeca = nodes_cabeca.new('ShaderNodeBsdfPrincipled')
    bsdf_cabeca.location = (0, 0)
    bsdf_cabeca.inputs["Base Color"].default_value = (0.3, 0.3, 0.3, 1.0)  # Cinza
    bsdf_cabeca.inputs["Roughness"].default_value = 0.9
    bsdf_cabeca.inputs["Specular"].default_value = 0.2
    
    # Adicionar textura Voronoi para a pedra
    voronoi_tex = nodes_cabeca.new('ShaderNodeTexVoronoi')
    voronoi_tex.location = (-300, 100)
    voronoi_tex.inputs["Scale"].default_value = 40.0
    
    # Adicionar textura de ruído para mais detalhes
    noise_tex2 = nodes_cabeca.new('ShaderNodeTexNoise')
    noise_tex2.location = (-300, -100)
    noise_tex2.inputs["Scale"].default_value = 80.0
    noise_tex2.inputs["Detail"].default_value = 10.0
    
    # Misturador para combinar as texturas
    mix_rgb = nodes_cabeca.new('ShaderNodeMixRGB')
    mix_rgb.location = (-150, 0)
    mix_rgb.inputs["Fac"].default_value = 0.7
    
    # Bump para dar relevo à textura
    bump = nodes_cabeca.new('ShaderNodeBump')
    bump.location = (-50, -200)
    bump.inputs["Strength"].default_value = 0.5
    
    # Ramp de cores para variações de cinza
    color_ramp2 = nodes_cabeca.new('ShaderNodeValToRGB')
    color_ramp2.location = (-150, 100)
    color_ramp2.color_ramp.elements[0].position = 0.3
    color_ramp2.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    color_ramp2.color_ramp.elements[1].position = 0.7
    color_ramp2.color_ramp.elements[1].color = (0.4, 0.4, 0.4, 1.0)
    
    # Saída do material
    output_cabeca = nodes_cabeca.new('ShaderNodeOutputMaterial')
    output_cabeca.location = (300, 0)
    
    # Conexões
    links_cabeca.new(voronoi_tex.outputs["Distance"], color_ramp2.inputs["Fac"])
    links_cabeca.new(color_ramp2.outputs["Color"], bsdf_cabeca.inputs["Base Color"])
    links_cabeca.new(noise_tex2.outputs["Fac"], bump.inputs["Height"])
    links_cabeca.new(bump.outputs["Normal"], bsdf_cabeca.inputs["Normal"])
    links_cabeca.new(bsdf_cabeca.outputs["BSDF"], output_cabeca.inputs["Surface"])
    
    # Material para as cordas
    material_corda = bpy.data.materials.new(name="Material_Corda")
    material_corda.use_nodes = True
    nodes_corda = material_corda.node_tree.nodes
    bsdf_corda = nodes_corda.get("Principled BSDF")
    if bsdf_corda:
        bsdf_corda.inputs["Base Color"].default_value = (0.55, 0.35, 0.15, 1.0)  # Marrom claro
        bsdf_corda.inputs["Roughness"].default_value = 1.0
        bsdf_corda.inputs["Specular"].default_value = 0.0
    
    return material_cabo, material_cabeca, material_corda

# Função principal para criar o machado
def criar_machado():
    # Criar as partes do machado
    cabo = criar_cabo()
    cabeca = criar_cabeca_machado()
    cordas = criar_cordas(cabo, cabeca)
    
    # Criar e atribuir materiais
    material_cabo, material_cabeca, material_corda = criar_materiais()
    
    # Atribuir material ao cabo
    cabo.data.materials.clear()
    cabo.data.materials.append(material_cabo)
    
    # Atribuir material à cabeça
    cabeca.data.materials.clear()
    cabeca.data.materials.append(material_cabeca)
    
    # Atribuir material às cordas
    for corda in cordas:
        corda.data.materials.clear()
        corda.data.materials.append(material_corda)
    
    # Adicionar rig (armature) para animar o machado
    bpy.ops.object.armature_add(enter_editmode=True, location=(-0.4, 0, 0))
    armature = bpy.context.active_object
    armature.name = "Armature_Machado"
    
    # Configurar ossos
    bone = armature.data.edit_bones[0]
    bone.name = "Bone_Handle"
    bone.tail = (0.1, 0, 0)
    
    # Adicionar um segundo osso para a cabeça
    head_bone = armature.data.edit_bones.new("Bone_Head")
    head_bone.head = (0.1, 0, 0)
    head_bone.tail = (0.5, 0, 0)
    head_bone.parent = bone
    
    # Finalizar a edição da armature
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Agrupar todos os objetos
    objetos_machado = [cabo, cabeca] + cordas
    for obj in objetos_machado:
        obj.select_set(True)
    
    bpy.context.view_layer.objects.active = cabo
    bpy.ops.object.join()
    machado = bpy.context.active_object
    machado.name = "Machado_Prehistorico"
    
    # Parenting com armature
    bpy.ops.object.select_all(action='DESELECT')
    machado.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # Adicionar um modificador de subdivisão para suavizar levemente o modelo
    bpy.context.view_layer.objects.active = machado
    bpy.ops.object.modifier_add(type='SUBSURF')
    machado.modifiers["Subdivision"].levels = 1
    machado.modifiers["Subdivision"].render_levels = 1
    
    # Definir a origem do objeto no centro do cabo para facilitar animações
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = (0, 0, 0)
    
    # Configurar visualização do viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
    
    return machado, armature

# Executar a função principal
machado, armature = criar_machado()

print("Machado de pedra pré-histórico criado com sucesso!")
