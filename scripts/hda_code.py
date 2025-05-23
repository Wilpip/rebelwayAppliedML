import hou
import math
import sys

sys.path.append(r"/home/wilpip/development/rebelwayAppliedML.git/a_star/scripts")

from a_star import AStarPathFinding

def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_colums = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    
    for row in range(num_rows):
        new_row = []
        for col in range(num_colums):
            prim_index = row * num_colums + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color ==(1.0,1.0,1.0) else 0)
            
        grid_matrix.append(new_row)
    

    return grid_matrix

def position_object(obj_path, row, col, cell_size=1):
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size
    
    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0 , world_z))
    pos = (row, col)
    return pos
    
def solve_maze():
    main_char_path = hou.pwd().parm("main_char").eval()
    
    npcs = [
        {"path": hou.pwd().parm("npc_1").eval(), "start_pos": (0, 3)},
        {"path": hou.pwd().parm("npc_2").eval(), "start_pos": (0, 6)},
        {"path": hou.pwd().parm("npc_3").eval(), "start_pos": (2, 3)}
    ]
    
    target_pos = position_object(main_char_path, 6, 1)
    
    maze = get_maze_from_grid()
    print("")
    for row in maze:
        print(row)
    
    all_paths = {}
    
    for i, npc in enumerate(npcs):
        row, col = npc["start_pos"]
        start_pos = position_object(npc["path"], row, col)
        
        pathFinder = AStarPathFinding(maze, start_pos, target_pos)
        path = pathFinder.find_path()
        
        if path:
            npc_name = f"npc_{i+1}"
            print(f"Path found for {npc_name}: {path}")
            all_paths[npc_name] = {"path": path, "npc_path": npc["path"]}
        else:
            print(f"No path found for NPC {i+1}!")
    
    if all_paths:
        return all_paths
    else:
        print("No paths found!")
        return None

def animate_npc():
    """
    Main animation function that calls solve_maze and animates all NPCs
    along their respective paths, with a movement every 4 frames.
    """
    # Appeler solve_maze pour trouver les chemins de tous les NPCs
    all_paths = solve_maze()
    
    if not all_paths:
        print("Animate impossible - no path found!")
        return
    
    cell_size = 1
    frames_per_step = 4
    
    start_frame = hou.playbar.frameRange()[0]
    max_path_length = 0
    
    for npc_name, data in all_paths.items():
        path = data["path"]
        npc_path = data["npc_path"]
        npc = hou.node(npc_path)
        
        max_path_length = max(max_path_length, len(path)) 
        print(f"Animation de {npc_name} sur {len(path)} positions")
        
        for i, pos in enumerate(path):
            row, col = pos
            world_x = col * cell_size
            world_z = row * cell_size
            
            current_frame = start_frame + i * frames_per_step
            hou.setFrame(current_frame)
            
            npc.parmTuple("t").set((world_x, 0, world_z))
            
            for j in range(3): 
                parm = npc.parm("t" + "xyz"[j])
                parm.setKeyframe(hou.Keyframe(parm.eval()))
    
    end_frame = start_frame + (max_path_length - 1) * frames_per_step
    hou.playbar.setPlaybackRange(start_frame, end_frame)
    
    hou.setFrame(start_frame)
    
    print(f"Animation create for {len(all_paths)} NPCs, at frame {start_frame} to {end_frame}")




