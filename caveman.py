import bpy
import math
import random

# Limpa a cena
def limpar_cena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Remove materiais não utilizados
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)
    
    # Remove malhas não utilizadas
    for mesh in bpy.data.meshes:
        if not mesh.users:
            bpy.data.meshes.remove(mesh)

# Cria materiais para o homem das cavernas
def criar_materiais():
    # Cor da pele
    mat_pele = bpy.data.materials.new(name="Pele")
    mat_pele.use_nodes = True
    bsdf = mat_pele.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.8, 0.6, 0.5, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Cabelo/Pelo
    mat_cabelo = bpy.data.materials.new(name="Cabelo")
    mat_cabelo.use_nodes = True
    bsdf = mat_cabelo.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.05, 0.02, 0.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 1.0
    
    # Roupa (pele animal)
    mat_roupa = bpy.data.materials.new(name="Roupa")
    mat_roupa.use_nodes = True
    bsdf = mat_roupa.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.6, 0.5, 0.3, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Clava (arma)
    mat_clava = bpy.data.materials.new(name="Clava")
    mat_clava.use_nodes = True
    bsdf = mat_clava.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.3, 0.2, 0.1, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    
    return {"pele": mat_pele, "cabelo": mat_cabelo, "roupa": mat_roupa, "clava": mat_clava}

# Cria o corpo do homem das cavernas
def criar_corpo(materiais):
    # Cria o torso
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
    torso = bpy.context.active_object
    torso.name = "Torso"
    torso.scale = (0.4, 0.3, 0.5)
    
    # Aplica o material da pele
    torso.data.materials.append(materiais["pele"])
    
    # Cabeça
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2))
    cabeca = bpy.context.active_object
    cabeca.name = "Cabeca"
    cabeca.scale = (0.3, 0.25, 0.3)
    cabeca.data.materials.append(materiais["pele"])
    
    # Braço esquerdo
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.7, 0, 1))
    braco_esq = bpy.context.active_object
    braco_esq.name = "BracoEsq"
    braco_esq.scale = (0.2, 0.2, 0.5)
    braco_esq.rotation_euler[2] = math.radians(-15)
    braco_esq.data.materials.append(materiais["pele"])
    
    # Antebraço esquerdo
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.1, 0, 0.5))
    antebraco_esq = bpy.context.active_object
    antebraco_esq.name = "AntebracoEsq"
    antebraco_esq.scale = (0.15, 0.15, 0.4)
    antebraco_esq.rotation_euler[2] = math.radians(-30)
    antebraco_esq.data.materials.append(materiais["pele"])
    
    # Braço direito
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.7, 0, 1))
    braco_dir = bpy.context.active_object
    braco_dir.name = "BracoDir"
    braco_dir.scale = (0.2, 0.2, 0.5)
    braco_dir.rotation_euler[2] = math.radians(15)
    braco_dir.data.materials.append(materiais["pele"])
    
    # Antebraço direito
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.1, 0, 0.5))
    antebraco_dir = bpy.context.active_object
    antebraco_dir.name = "AntebracoDir"
    antebraco_dir.scale = (0.15, 0.15, 0.4)
    antebraco_dir.rotation_euler[2] = math.radians(30)
    antebraco_dir.data.materials.append(materiais["pele"])
    
    # Perna esquerda
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.2, 0, 0))
    perna_esq = bpy.context.active_object
    perna_esq.name = "PernaEsq"
    perna_esq.scale = (0.15, 0.2, 0.5)
    perna_esq.data.materials.append(materiais["pele"])
    
    # Perna direita
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.2, 0, 0))
    perna_dir = bpy.context.active_object
    perna_dir.name = "PernaDir"
    perna_dir.scale = (0.15, 0.2, 0.5)
    perna_dir.data.materials.append(materiais["pele"])
    
    # Acrescenta detalhes da cabeça
    # Nariz
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.3, 2))
    nariz = bpy.context.active_object
    nariz.name = "Nariz"
    nariz.scale = (0.1, 0.1, 0.1)
    nariz.data.materials.append(materiais["pele"])
    
    # Mandíbula proeminente
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, 1.8))
    mandibula = bpy.context.active_object
    mandibula.name = "Mandibula"
    mandibula.scale = (0.25, 0.15, 0.1)
    mandibula.data.materials.append(materiais["pele"])
    
    # Sobrancelhas
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.15, 0.25, 2.15))
    sobrancelha_esq = bpy.context.active_object
    sobrancelha_esq.name = "SobrancelhaEsq"
    sobrancelha_esq.scale = (0.1, 0.05, 0.02)
    sobrancelha_esq.data.materials.append(materiais["cabelo"])
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.15, 0.25, 2.15))
    sobrancelha_dir = bpy.context.active_object
    sobrancelha_dir.name = "SobrancelhaDir"
    sobrancelha_dir.scale = (0.1, 0.05, 0.02)
    sobrancelha_dir.data.materials.append(materiais["cabelo"])
    
    # Cabelo/Barba
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.35))
    cabelo = bpy.context.active_object
    cabelo.name = "Cabelo"
    cabelo.scale = (0.32, 0.27, 0.1)
    cabelo.data.materials.append(materiais["cabelo"])
    
    # Barba
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, 1.7))
    barba = bpy.context.active_object
    barba.name = "Barba"
    barba.scale = (0.25, 0.15, 0.2)
    barba.data.materials.append(materiais["cabelo"])
    
    # Adiciona roupa de pele animal
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.7))
    roupa = bpy.context.active_object
    roupa.name = "Roupa"
    roupa.scale = (0.42, 0.32, 0.25)
    roupa.data.materials.append(materiais["roupa"])
    
    # Adiciona uma clava (arma)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1, location=(-1.5, 0, 0.5))
    clava_handle = bpy.context.active_object
    clava_handle.name = "ClavaHandle"
    clava_handle.rotation_euler[0] = math.radians(90)
    clava_handle.data.materials.append(materiais["clava"])
    
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.2, subdivisions=1, location=(-1.5, -0.5, 0.5))
    clava_head = bpy.context.active_object
    clava_head.name = "ClavaHead"
    clava_head.data.materials.append(materiais["clava"])
    
    # Coloca vértices aleatórios para efeito low-poly nas malhas
    objetos = [torso, cabeca, braco_esq, braco_dir, antebraco_esq, antebraco_dir, 
               perna_esq, perna_dir, nariz, mandibula, sobrancelha_esq, sobrancelha_dir,
               cabelo, barba, roupa, clava_handle, clava_head]
    
    for obj in objetos:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=1)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Adiciona variação de vértices para efeito mais orgânico/low-poly
        for vertex in obj.data.vertices:
            vertex.co.x += random.uniform(-0.02, 0.02)
            vertex.co.y += random.uniform(-0.02, 0.02)
            vertex.co.z += random.uniform(-0.02, 0.02)
    
    # Cria um grupo de objetos para o homem das cavernas
    todas_partes = objetos
    
    # Seleciona todos os objetos
    for obj in todas_partes:
        obj.select_set(True)
    
    bpy.context.view_layer.objects.active = torso
    
    return todas_partes

# Cria armature (esqueleto) para animação
def criar_armature(partes_do_corpo):
    # Cria a armature
    bpy.ops.object.armature_add(location=(0, 0, 0))
    armature = bpy.context.active_object
    armature.name = "CavemanArmature"
    
    # Entra no modo de edição
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Remove o bone padrão
    for bone in armature.data.edit_bones:
        armature.data.edit_bones.remove(bone)
    
    # Cria os bones
    # Torso (root)
    root = armature.data.edit_bones.new('Root')
    root.head = (0, 0, 0)
    root.tail = (0, 0, 1)
    
    # Spine
    spine = armature.data.edit_bones.new('Spine')
    spine.head = (0, 0, 1)
    spine.tail = (0, 0, 1.5)
    spine.parent = root
    
    # Cabeça
    head = armature.data.edit_bones.new('Head')
    head.head = (0, 0, 1.5)
    head.tail = (0, 0, 2)
    head.parent = spine
    
    # Braço esquerdo
    arm_l = armature.data.edit_bones.new('ArmL')
    arm_l.head = (0.4, 0, 1.5)
    arm_l.tail = (0.7, 0, 1)
    arm_l.parent = spine
    
    # Antebraço esquerdo
    forearm_l = armature.data.edit_bones.new('ForearmL')
    forearm_l.head = (0.7, 0, 1)
    forearm_l.tail = (1.1, 0, 0.5)
    forearm_l.parent = arm_l
    
    # Mão esquerda
    hand_l = armature.data.edit_bones.new('HandL')
    hand_l.head = (1.1, 0, 0.5)
    hand_l.tail = (1.3, 0, 0.4)
    hand_l.parent = forearm_l
    
    # Braço direito
    arm_r = armature.data.edit_bones.new('ArmR')
    arm_r.head = (-0.4, 0, 1.5)
    arm_r.tail = (-0.7, 0, 1)
    arm_r.parent = spine
    
    # Antebraço direito
    forearm_r = armature.data.edit_bones.new('ForearmR')
    forearm_r.head = (-0.7, 0, 1)
    forearm_r.tail = (-1.1, 0, 0.5)
    forearm_r.parent = arm_r
    
    # Mão direita
    hand_r = armature.data.edit_bones.new('HandR')
    hand_r.head = (-1.1, 0, 0.5)
    hand_r.tail = (-1.3, 0, 0.4)
    hand_r.parent = forearm_r
    
    # Objeto da clava
    clava = armature.data.edit_bones.new('Clava')
    clava.head = (-1.3, 0, 0.4)
    clava.tail = (-1.5, -0.5, 0.5)
    clava.parent = hand_r
    
    # Perna esquerda
    thigh_l = armature.data.edit_bones.new('ThighL')
    thigh_l.head = (0.2, 0, 0.5)
    thigh_l.tail = (0.2, 0, 0)
    thigh_l.parent = root
    
    # Pé esquerdo
    foot_l = armature.data.edit_bones.new('FootL')
    foot_l.head = (0.2, 0, 0)
    foot_l.tail = (0.2, 0.2, 0)
    foot_l.parent = thigh_l
    
    # Perna direita
    thigh_r = armature.data.edit_bones.new('ThighR')
    thigh_r.head = (-0.2, 0, 0.5)
    thigh_r.tail = (-0.2, 0, 0)
    thigh_r.parent = root
    
    # Pé direito
    foot_r = armature.data.edit_bones.new('FootR')
    foot_r.head = (-0.2, 0, 0)
    foot_r.tail = (-0.2, 0.2, 0)
    foot_r.parent = thigh_r
    
    # Volta para o modo objeto
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Seleciona todas as partes do corpo
    for obj in partes_do_corpo:
        obj.select_set(True)
    
    # Seleciona a armature como o objeto ativo
    bpy.context.view_layer.objects.active = armature
    
    # Adiciona o modificador Armature a todas as partes
    # Adiciona os modificadores de armadura a cada parte do corpo
    for obj in partes_do_corpo:
        modifier = obj.modifiers.new(name="Armature", type='ARMATURE')
        modifier.object = armature
    
    # Retorna a armature
    return armature

# Cria uma pose padrão
def criar_pose_padrao(armature):
    # Muda para o modo pose
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Pose do braço direito para segurar a clava
    armature.pose.bones["ArmR"].rotation_euler[2] = math.radians(25)
    armature.pose.bones["ForearmR"].rotation_euler[2] = math.radians(40)
    
    # Pose do braço esquerdo
    armature.pose.bones["ArmL"].rotation_euler[2] = math.radians(-25)
    armature.pose.bones["ForearmL"].rotation_euler[2] = math.radians(-40)
    
    # Pose das pernas (levemente afastadas)
    armature.pose.bones["ThighL"].rotation_euler[1] = math.radians(10)
    armature.pose.bones["ThighR"].rotation_euler[1] = math.radians(-10)
    
    # Volta para o modo objeto
    bpy.ops.object.mode_set(mode='OBJECT')

# Função principal
def criar_homem_das_cavernas():
    # Limpa a cena
    limpar_cena()
    
    # Cria materiais
    materiais = criar_materiais()
    
    # Cria o corpo
    partes_do_corpo = criar_corpo(materiais)
    
    # Cria armature
    armature = criar_armature(partes_do_corpo)
    
    # Cria pose padrão
    criar_pose_padrao(armature)
    
    # Centraliza a visão na armature
    armature.select_set(True)
    bpy.ops.view3d.view_selected()
    
    return armature

# Executa o script
if __name__ == "__main__":
    criar_homem_das_cavernas()
