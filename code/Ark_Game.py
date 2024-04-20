# 注：建议使用Python1.12.2版本，若版本过低，可能会出现无法运行的情况
# 请注意时间，不能将时间手动调为1970年1月1日0点0分以前！
# 版权所有：writing
import os
import json
import time
import random
import tempfile
print("检查依赖...")
print("检查/下载脚本正在执行✨")
os.system("pip install ursina -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn/simple");os.system("pip install pillow");os.system("pip install perlin_noise")
print("依赖检查完毕...")
from ursina import *
from threading import *
from perlin_noise import PerlinNoise
import PIL.Image as Image
from ursina.prefabs.first_person_controller import FirstPersonController
app=Ursina(title="Ark Game β 0.5")
print("欢迎你,版本:😃开发者预览版0.5")
const_TMP_PATH=tempfile.gettempdir()
mouse.locked = True;mouse.visible = False
user_HandBlock=None
user_OccupyMouse=True
resource_bag_block_dict={}
resource_block_time_dict={}
resource_texture_dict={}
def_const_num={}
def_block_postion={}
def_system_data={"json_data":None,"user_json":None,"game_data":{},'page':"Index","careful":"Main","game":None,'en':True,"entity":{},"system_data":{"appdata":os.getenv('APPDATA')+"/.Ark"},"block":{}}#block为方块注册表
def ToAbs(path,mount="."):
    return os.path.abspath(os.path.join(mount, path))
def Tailor(json_data,path,Dict_Block,Dict_Block_time):
    run_path=ToAbs(def_system_data["json_data"]["load_texture"],mount=path)
    img=Image.open(run_path)
    idx=0
    break_flag=False
    tmp_list_key=list(json_data["texture"].keys())
    tmp_list_value=list(json_data["texture"].values())
    for i in range(0,json_data["y"]*json_data["w"],json_data["h"]):
        if break_flag:
            break
        for j in range(0,json_data["x"]*json_data["h"],json_data["w"]):
            CropFileSave(run_path ,Crop_data=[j,i,json_data["h"],json_data["w"],const_TMP_PATH,json_data["load_texture"]+str(i/json_data["h"])+"_"+str(j/json_data["w"])])
            Dict_Block[str(tmp_list_key[idx]).lower()]=load_texture(json_data["load_texture"]+str(i/json_data["h"])+"_"+str(j/json_data["w"])+".png",path=const_TMP_PATH)
            Dict_Block_time[str(tmp_list_key[idx]).lower()]=tmp_list_value[idx]
            if idx>=json_data["texture_load_amount"]:
                break_flag=True
                break
            idx+=1
def CropFileSave(path,Crop_data=[0,0,0,0,const_TMP_PATH,"hello"]):
    img=Image.open(path)
    img=img.crop((Crop_data[0],Crop_data[1],Crop_data[0]+Crop_data[2],Crop_data[1]+Crop_data[3]))
    return img.save(Crop_data[4]+"/"+Crop_data[5]+".png")
def input_down(key):
    print(key)
    if def_system_data["game"]!=None:
        if key=="left mouse down" and def_system_data["game_data"]["run_Block"]:
            def_system_data["game_data"]["block_time"]=def_system_data["game_data"]["time"]
def input_up(key, is_raw=False):
    print(key)
    if def_system_data["game"]!=None:
        if key=="left mouse up" and def_system_data["game_data"]["run_Block"]:
            if def_system_data["game_data"]["block_time"]>=def_system_data["game_data"]["run_Block"].block_time:
                destroy(def_system_data["game_data"]["run_Block"])
            def_system_data["game_data"]["block_time"]=-1
def input(key):
    if def_system_data["page"]=="Game":
        def_system_data["game"].input(key)
def update():
    global user_OccupyMouse,def_system_data,user_HandBlock,resource_bag_block_dict
    #系统级别update
    if not def_system_data["en"]:
        if def_system_data["page"]=="Game":
            def_system_data["game"].delete()
        exit()
    def_system_data["game_data"]['fps']=window.fps_counter.text
    def_system_data["game_data"]["time"]=time.time()
    #处理不同任务update
    if def_system_data["page"]=="Index" and def_system_data["game"]!=None:
        def_system_data["game"].delete()
        print("删除成功")
        def_system_data["game"]=None
    if def_system_data["page"]=="Game":
        def_system_data["game"].update()
def IndexToKey(index,Dict):
    tmp_list=list(Dict.keys())
    return tmp_list[index]
def IndexToValue(index,Dict):
    tmp_list=list(Dict.values())
    return tmp_list[index]
def FindKeyByValue(Key,Dict):
    tmp_list=list(Dict.values())
    return list(Dict.keys())[tmp_list.index(Key)]
def FindValueByKey(values,Dict):
    tmp_list=list(Dict.values())   
def DeathVerdict(position,hp):
    if hp<=0:
        return True
    elif position.y<=-10:
        return True
    else:
        return False    
class Title(Entity):   
    old_position=(0,0) 
    exit_button=None
    minimize=None
    maximize=None
    def __init__(self,**kwargs):
        window.fps_counter.visible = False;window.collider_counter.visible = False;window.entity_counter.visible = False;window.exit_button.enabled=False;window.fullscreen=False;window.minimized=False
        text=Text(text=kwargs['text'],position=(-0.1,0.5),parent=camera.ui,z=3,font=".\\MiSans-Light.ttf")
        text.position=(-1*(float(text.width)/2),0.5,0)
        super().__init__(model='cube',position=(0,0.5),parent=camera.ui,scale=(2,0.06),color=color.gray,z=4)
        self.exit_button=Button(model="sphere",text='X',parent=camera.ui,scale=(0.03,0.03),position=(0.873,0.485),z=2,color=color.red,text_color=color.black)
        self.maximize=Button(model="sphere",text='O',parent=camera.ui,scale=(0.03,0.03),position=(0.843,0.485),z=2,color=color.green,text_color=color.black)
        self.minimize=Button(model="sphere",text='_',parent=camera.ui,scale=(0.03,0.03),position=(0.813,0.485),z=2,color=color.yellow,text_color=color.black)
    def update(self):
        pass
    def input(self,key):
        if self.minimize.hovered and key=='left mouse down':
            global user_OccupyMouse
            window.minimized=True
            def_system_data["entity"]["player"].enabled=not(def_system_data["entity"]["player"].enabled)
            def_system_data["entity"]["player"].enabled=not(def_system_data["entity"]["player"].enabled)
            window.minimized=False
        elif self.maximize.hovered and key=='left mouse down':
            window.minimized=False
            window.fullscreen=not(window.fullscreen)
            window.minimized=True
        elif self.exit_button.hovered and key=='left mouse down':
            def_system_data['en']=False
            print("正在通知所有进程关闭")
        else :
            window.minimized=False
class Game():
    class Scene():
        class Sky(Entity):
            def __init__(self):
                global resource_texture_dict,def_system_data
                super().__init__(parent=scene,model="sphere",scale=def_system_data["game_data"]["scale"],texture=resource_texture_dict["sky"],double_sided=True,position=(0,0,0))
        class Block(Button):
            block_time=0
            global resource_block_time_dict
            def __init__(self,position=(0,0,0),texture=user_HandBlock,key="user"):
                global def_system_data,def_block_postion,resource_block_time_dict,resource_texture_dict
                if key=="user":
                    if def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]['HandBlock']]<=0:
                        def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]['HandBlock']]=0
                        del self
                    else:
                        def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]['HandBlock']]-=1
                        super().__init__(parent=scene,position=position,model="cube",highlight_color=color.gray,color=color.white,texture=texture,origin_y=0.5,collider='box')
                        #进行方块注册
                        def_system_data["block"][position]=self
                        self.block_time=resource_block_time_dict[FindKeyByValue(texture,resource_texture_dict)]
                elif key=="system":
                    super().__init__(parent=scene,position=position,model="cube",highlight_color=color.gray,color=color.white,texture=texture,origin_y=0.5,collider='box')
                    #进行方块注册
                    def_system_data["block"][position]=self
                    self.block_time=resource_block_time_dict[FindKeyByValue(texture,resource_texture_dict)]
                else:
                    print_warning("未知的key")
                    del self
        class Falling(Entity):
            init_y=0
            def __init__(self,position=(0,0,0),texture=None):
                super().__init__(position=position,texture=texture,scale=(0.2,0.2,0.2),model="cube",collider="box")
                self.init_y=position[1]
            def PickUp(self):
                global resource_bag_block_dict
                bag_value=list(resource_bag_block_dict.values())
                flag = False
                while True:
                    if not (self.texture in bag_value):
                        break
                    elif def_system_data["game_data"]["def_bag_list"][bag_value.index(self.texture)]<64:
                        def_system_data["game_data"]["def_bag_list"][bag_value.index(self.texture)]+=1
                        destroy(self)
                        flag=True
                        break
                    else:
                        bag_value[bag_value.index(self.texture)]=None
                        continue
                if flag:
                   return 
                else:
                    bag_value=list(resource_bag_block_dict.values())
                    while True:
                        if not (None in bag_value):
                            break
                        else:
                            def_system_data["game_data"]["def_bag_list"][bag_value.index(None)]+=1
                            resource_bag_block_dict[bag_value.index(None)]=self.texture
                            destroy(self)
                            break
                    return 
            def update(self):
                self.rotation_y+=2
                if not self.intersects().hit:
                    self.y-=0.5
                if self.intersects():
                    if self.intersects().hit and not self.intersects(def_system_data["entity"]["player"]).hit and type(self.intersects().entity)!=type(self):
                        self.y+=0.5
                        if self.y>self.init_y:
                            self.y=self.init_y-0.5
                if self.intersects(def_system_data["entity"]["player"]).hit: 
                    self.PickUp()
                if self.intersects(def_system_data["entity"]["sky"]).hit:
                    destroy(self)  
        class Backpack():
            class cell(Entity):
                idx=0
                text=None
                def __init__(self,position=(0,0),index=0):
                    global user_HandBlock,def_system_data,resource_bag_block_dict
                    self.backdrop=Entity(position=position,model="cube",parent=camera.ui,scale=(0.1,0.1),color=(0,0,0.5,0.33),z=8)
                    super().__init__(position=position,model="cube",parent=camera.ui,scale=(0.09,0.09),texture=IndexToValue(index,resource_bag_block_dict),z=6)
                    self.idx=index
                    if index!=-1:
                        self.id=Text(text=str((self.idx+1)%10),position=self.position+(0,-0.05),color=color.white,parent=camera.ui,z=8)
                    self.text=Text(text=str(def_system_data["game_data"]["def_bag_list"][self.idx]),position=self.position+(0.02,-0.02),color=color.white,parent=camera.ui)
                    self.backdrop.color=color.gray
                def update(self):
                    self.text.z=6
                    self.z=7
                    if def_system_data["game_data"]["Hand_ID"]==self.idx:
                        self.texture=None;self.text.text=""
                    else:
                        self.text.text=str(def_system_data["game_data"]["def_bag_list"][self.idx])
                        self.texture=IndexToValue(self.idx,resource_bag_block_dict)
                    if def_system_data["game_data"]["HandBlock"]==self.idx:
                        self.backdrop.color=color.yellow
                        self.backdrop.scale=(0.105,0.105)
                        self.scale=(0.095,0.095)
                        self.backdrop.z=7
                        self.z=6
                    else:
                        self.backdrop.color=color.gray
                        self.backdrop.scale=(0.1,0.1)
                        self.scale=(0.09,0.09)
                        self.backdrop.z=8
                        self.z=6
                def input(self,key):
                    if key=="q" and def_system_data["game_data"]["HandBlock"]==self.idx:
                        pos=def_system_data["entity"]["player"].forward*2+def_system_data["entity"]["player"].position
                        if def_system_data["game_data"]["def_bag_list"][self.idx]>0:
                            Falling(position=pos+(0,0.3,0),texture=resource_bag_block_dict[self.idx])
                            def_system_data["game_data"]["def_bag_list"][self.idx]-=1
                    if key=="f" and def_system_data["game_data"]["HandBlock"]==self.idx:
                        tmp_data=def_system_data["game_data"]["def_bag_list"][-1]
                        tmp_data_2=resource_bag_block_dict[-1]
                        resource_bag_block_dict[-1] = resource_bag_block_dict[self.idx]
                        def_system_data["game_data"]["def_bag_list"][-1]=def_system_data["game_data"]["def_bag_list"][self.idx]
                        resource_bag_block_dict[-1] = tmp_data_2
                        def_system_data["game_data"]["def_bag_list"][self.idx]=tmp_data

                def delete(self):
                    destroy(self.text)
                    if self.idx!=-1:
                        destroy(self.id)
                    destroy(self.backdrop)
                    destroy(self)
            def __init__(self):
                global def_system_data
                j=0
                def_system_data["entity"]["backpack_cell"]=[]
                for i in range(-5,5,1):
                    def_system_data["entity"]["backpack_cell"].append(self.cell(position=((i/10)+0.05,-0.42),index=j)) 
                    j+=1
                def_system_data["entity"]["backpack_cell"].append(self.cell(position=(-0.6,-0.42),index=-1))
                print(def_system_data["game_data"]["def_bag_list"])
        class Bag(Entity):      
            entity=None
            class Hand_Block(Entity):
                text=None
                def __init__(self):
                    super().__init__(texture=None,position=(1,1),z=1,parent=camera.ui,model="cube",scale=(0.045,0.045),Z=10)
                    self.text=Text(text=str(0), position=self.position+(-0.001,0.001), color=color.white,parent=camera.ui,Z=1)
                    self.text.visible=False
                    self.visible=False
                def update(self):
                    global resource_bag_block_dict,def_system_data
                    if def_system_data["game_data"]["Hand_ID"]!=-1 and IndexToValue(def_system_data["game_data"]["Hand_ID"],resource_bag_block_dict)!=None:
                        self.visible=True
                        self.text.visible=True
                        self.text.position=self.position+(-0.001,0,-1)
                        self.position=mouse.position
                        self.texture=IndexToValue(def_system_data["game_data"]["Hand_ID"],resource_bag_block_dict)
                        self.text.text=def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]["Hand_ID"]]
                    else:
                        self.visible=False
                        self.text.visible=False
                        self.position=(1,1)
                def delete(self):
                    destroy(self.text)
                    destroy(self)
            class cell(Button):
                idx=0
                Hovered=False
                text=None
                mov=False
                def __init__(self,position=(0,0),index=0,parent=camera.ui):
                    global user_HandBlock,def_system_data
                    self.backdrop=Entity(position=position,model="cube",parent=parent,scale=(0.05,0.05),color=color.gray,z=3)
                    textures=IndexToValue(index,resource_bag_block_dict)
                    super().__init__(position=position,model="cube",parent=camera.ui,color=color.white,scale=(0.045,0.045),texture=IndexToValue(index,resource_bag_block_dict),collider='box',z=2)
                    self.text=Text(text=str(def_system_data["game_data"]["def_bag_list"][self.idx]), position=position+(-0.001,0), color=color.white,parent=camera.ui,z=1)
                    self.idx=index;self.backdrop.color=color.gray;self.backdrop.visible= False;self.visible=False;self.text.visible=False
                def input(self,key):
                    if self.Hovered and self.visible:
                        if key=="left mouse down" and def_system_data["game_data"]["Hand_ID"]==-1:
                            def_system_data["game_data"]["Hand_ID"]=self.idx
                            def_system_data["game_data"]["up"]=False
                            self.mov=True
                        #以下代码用于防抖
                        if key=="left mouse up" and def_system_data["game_data"]["Hand_ID"]!=-1:
                            def_system_data["game_data"]["up"]=True
                        if key=="left mouse down" and def_system_data["game_data"]["Hand_ID"]!=-1:
                            if def_system_data["game_data"]["Hand_ID"]==self.idx and def_system_data["game_data"]["up"]:
                                def_system_data["game_data"]["Hand_ID"]=-1
                                self.mov=False
                            else:
                                    tmp=resource_bag_block_dict[IndexToKey(self.idx,resource_bag_block_dict)]
                                    resource_bag_block_dict[IndexToKey(self.idx,resource_bag_block_dict)]=resource_bag_block_dict[IndexToKey(def_system_data["game_data"]["Hand_ID"],resource_bag_block_dict)]
                                    resource_bag_block_dict[IndexToKey(def_system_data["game_data"]["Hand_ID"],resource_bag_block_dict)]=tmp
                                    tmp_1=def_system_data["game_data"]["def_bag_list"][self.idx]
                                    def_system_data["game_data"]["def_bag_list"][self.idx]=def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]["Hand_ID"]]
                                    def_system_data["game_data"]["def_bag_list"][def_system_data["game_data"]["Hand_ID"]]=tmp_1
                    if key=="escape" and not def_system_data["game_data"]["bag_open"]:
                        self.backdrop.visible=not(self.backdrop.visible) ; self.visible=not(self.visible) ; self.text.visible=not(self.text.visible)
                    if key=="e":
                        self.backdrop.visible=not(self.backdrop.visible) ; self.visible=not(self.visible) ; self.text.visible=not(self.text.visible)
                def update(self): 
                    global resource_bag_block_dict,def_system_data
                    if def_system_data["game_data"]["def_bag_list"][self.idx]==0:
                        resource_bag_block_dict[self.idx]=None
                    if self.hovered:
                        self.Hovered=True
                    if not self.hovered:
                        self.Hovered=False
                    if not self.visible:
                        self.mov=False
                    self.texture=IndexToValue(self.idx,resource_bag_block_dict)
                    if self.texture==None:
                        def_system_data["game_data"]["def_bag_list"][self.idx]=0
                        self.text.text=""
                    if def_system_data["game_data"]["def_bag_list"][self.idx]==0:
                        resource_bag_block_dict[self.idx]==None
                    if self.mov == True:
                        self.texture=None;self.text.text=""
                        def_system_data["game_data"]["Hand_Block"]=self
                    else:
                        self.texture=IndexToValue(self.idx,resource_bag_block_dict)
                        if def_system_data["game_data"]["def_bag_list"][self.idx]!=0:
                            self.text.text=def_system_data["game_data"]["def_bag_list"][self.idx]
                def delete(self):
                    destroy(self.text)
                    destroy(self.backdrop)
                    destroy(self)
            def __init__(self):
                super().__init__(model="cube", parent=camera.ui, scale=(0.5, 0.55), color=(0, 0, 0), position=(0, 0),z=4)
                layer=-10
                self.visible=False
                idx=0
                self.Hand=self.Hand_Block()
                def_system_data["entity"]["bag_cell"]=[]
                for j in range(-5,5,1):
                    def_system_data["entity"]["bag_cell"].append(self.cell(position=((j/20)+0.025,-0.25),index=idx))
                    idx+=1
                for i in range(1,5,1):
                    for j in range(-5,5,1):
                        def_system_data["entity"]["bag_cell"].append(self.cell(position=((j/20)+0.025,-0.22+(i/20)),index=idx))
                        idx+=1
            def input(self,key):
                global user_OccupyMouse
                if key=="escape" and not def_system_data["game_data"]["bag_open"]:
                    def_system_data["game_data"]["bag_open"]=True
                if (key == "e") and (user_OccupyMouse and not def_system_data["game_data"]["bag"] or not user_OccupyMouse and def_system_data["game_data"]["bag"]):
                    self.visible=not(self.visible)
                    def_system_data["entity"]["player"].enabled=not(def_system_data["entity"]["player"].enabled)
                    def_system_data["game_data"]["bag"]=not(def_system_data["game_data"]["bag"])
                    mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse) 
                if key == "escape" and not user_OccupyMouse and def_system_data["game_data"]["bag"]:
                    def_system_data["entity"]["player"].enabled=True
                    self.visible=False;def_system_data["game_data"]["bag"]=False;def_system_data["game_data"]["bag_open"]=False
                    mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse)
                if key == "e" and not user_OccupyMouse and not def_system_data["game_data"]["bag"]:
                    self.visible=not(self.visible)
                    def_system_data["entity"]["player"].enabled=not(def_system_data["entity"]["player"].enabled)
                    def_system_data["game_data"]["bag_open"]=def_system_data["game_data"]["bag"]=not(def_system_data["game_data"]["bag"])
                    mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse)
            def update(self):
                global def_system_data
                if not self.visible:
                    def_system_data["game_data"]["Hand_ID"]=-1
            def delete(self):
                for i in def_system_data["entity"]["bag_cell"]:
                    i.delete()
                self.Hand.delete()
        class Quest(Thread):
            def __init__(self):
                super().__init__()
                print("start")
            def distance(self,entity1=(0,0,0),entity2=(0,0,0)):
                ans=0
                for i in range(3):
                    ans+=math.pow(entity1[i]-entity2[i],2)
                ans=math.sqrt(ans)
                return ans
            def run(self):
                while def_system_data["en"]:
                    if held_keys["w"] or held_keys["s"] or held_keys["a"] or held_keys["d"]:
                        for tmp in def_system_data["block"]:
                            pass
                    # pass 
        class Options(Entity):
            restart=None
            title_screen=None
            def Return_to_title_screen(self):
                print("main")
                def_system_data['page']="Index"
                def_system_data['careful']="Map"
                print(def_system_data['page'],def_system_data['careful'])
                self.restart.enabled=False
                self.title_screen.enabled=False
                self.color=Color(0, 0, 0, 0.75)
            def Restart(self):
                print("restart")
                def_system_data["entity"]["player"].position=(def_system_data["game_data"]["start_x"],def_system_data["game_data"]["start_z"],def_system_data["game_data"]["start_y"])
                def_system_data["entity"]["player"].enabled = True
                self.restart.enabled=False
                self.title_screen.enabled=False
                self.color=Color(0, 0, 0, 0.75)    
            def Death(self):
                self.visible=True
                def_system_data["entity"]["player"].enabled = False
                self.restart.enabled=True
                self.title_screen.enabled=True
                self.color=Color(0, 0, 0, 0.85)
            def __init__(self):
                self.restart=Button(text="Second Life...",position=(0,0.1),color=Color(1, 1, 0, 0.75),z=4,parent=camera.ui,scale=(0.4,0.1),enabled=False)
                self.title_screen=Button(text="Main Menu",position=(0,-0.1),color=Color(1, 1, 0, 0.75),z=4,parent=camera.ui,scale=(0.4,0.1),enabled=False)
                super().__init__(model="cube",scale=(5,5),parent=camera.ui,position=(0,0),color=Color(0, 0, 0, 0.75),z=5)
                self.visible = False
            def input(self,key):
                if self.restart.hovered and key=="left mouse down":
                    self.Restart()
                elif self.title_screen.hovered and key=="left mouse down":
                    print("hello")
                    self.Return_to_title_screen()
                self.visible = mouse.visible
                if key=="escape" and self.visible:
                    self.title_screen.enabled=True
                elif key=="escape":
                    self.title_screen.enabled=False
        class Hand(Entity):
            def __init__(self):
                super().__init__(
                    parent=camera.ui,
                    model="cube",
                    scale=(0.18,0.18),
                    color=color.white,
                    texture="white_cube",
                    rotation=Vec3(150,-10,0),
                    position=(0.64,-0.65),
                    z=10
                )
            def active(self):
                self.position=(0.60,-0.65)
                self.rotation=Vec3(150,-20,0)
            def passive(self):
                self.position=(0.64,-0.65)
                self.rotation=Vec3(150,-10,0)
        def update(self):
            user_HandBlock=IndexToValue(def_system_data["game_data"]["HandBlock"],resource_bag_block_dict)
            print(def_system_data["entity"]["player"].forward)
            if held_keys["left mouse"] or held_keys["right mouse"]:
                def_system_data["entity"]["hand"].active()
            else:
                def_system_data["entity"]["hand"].passive()
            if DeathVerdict(def_system_data["entity"]["player"].position,def_system_data["game_data"]["HP"]):
                if(def_system_data["json_data"]["rebirth"]=="True"):
                    def_system_data["entity"]["options"].Death()
                    def_system_data["game_data"]["HP"]=def_system_data["json_data"]["HP"]
        def input(self,key):
            global user_OccupyMouse
            if key.isdigit():
                def_system_data["game_data"]['HandBlock']=int(key)-1
                if key=='0':
                        def_system_data["game_data"]['HandBlock']=9
            if key=="escape" and not(def_system_data["game_data"]["bag"]):
                window.minimized=False
                def_system_data["entity"]["player"].enabled=not(def_system_data["entity"]["player"].enabled)
                mouse.visible = not(mouse.visible)
                user_OccupyMouse=not(user_OccupyMouse)  
                window.minimized=True
        def __init__(self,**kwargs):
            def_system_data["page"]="Game"            
            global resource_texture_dict,resource_block_time_dict
            def_system_data["json_data"]=json.load(open(kwargs['package']+"/config.json",'r'))
            def_system_data["user_json"]=json.load(open(kwargs['package']+"/user_config.json",'r'))
            Tailor(def_system_data["json_data"],kwargs['package'],resource_texture_dict,resource_block_time_dict)
            nosie=PerlinNoise(octaves=2.5,seed=def_system_data["json_data"]["seed"])
            scale = 24
            def_system_data["game_data"]={"bag":False,"bag_open":True,"Hand_Block":None,"Hand_ID":-1,"up":False,'HandBlock':0,'run_Block':None,"block_time":-1,"start_x":def_system_data["user_json"]["x"],"start_y":def_system_data["user_json"]["y"],"start_z":def_system_data["user_json"]["y"],"def_bag_list":[],"r":def_system_data["user_json"]["r"]}
            def_system_data["game_data"]["HP"]=def_system_data["json_data"]["HP"]
            def_system_data["game_data"]["scale"]=def_system_data["json_data"]["scale"]
            def_system_data["entity"]["hand"]=self.Hand()
            for i in range(0,50): 
                resource_bag_block_dict[i]=resource_texture_dict["dirt"]
                def_system_data["game_data"]["def_bag_list"].append(i)
            def_system_data["entity"]["backpack"]=self.Backpack()
            def_system_data["entity"]["bag"]=self.Bag()
            def_system_data["entity"]["sky"]=self.Sky()
            def_system_data["entity"]["options"]=self.Options()
            def_system_data["entity"]["player"]=FirstPersonController(collider="box",position=(def_system_data["game_data"]["start_x"],def_system_data["game_data"]["start_z"],def_system_data["game_data"]["start_y"]))
            def_system_data["entity"]["player"].enabled=True
            isa=0 
            for z in range(-20,20):
                for x in range(-20,10):
                    user_HandBlock=None
                    i=int(nosie([x/scale,z/scale])*10)
                    self.Block(position=(x,i,z),texture=resource_texture_dict["dirt"],key="system")
                    for y in range(-2,i):
                        self.Block(position=(x,y,z),texture=resource_texture_dict["dirt"],key="system")
            quest=self.Quest()
            quest.start()
        def delete(self):
            global def_system_data 
            def_system_data["page"]="Index"
            def_system_data["careful"]="Map"
            def_system_data["entity"]["bag"].delete();destroy(def_system_data["entity"]["bag"]);destroy(def_system_data["entity"]["sky"]);destroy(def_system_data["entity"]["options"]);destroy(def_system_data["entity"]["player"])
            del def_system_data["entity"]["backpack"]
            print(def_system_data["entity"]["player"])
            def_system_data["entity"]["bag"]=None
            def_system_data["entity"]["sky"]=None
            def_system_data["entity"]["options"]=None
            def_system_data["entity"]["player"]=None
            for i in def_system_data["entity"]["backpack_cell"]:
                i.delete()
    def __init__(self,package,scene):
        self.package=package
        self.game_scaner=self.Scene(package=package+"/"+scene)
    def update(self):
        self.game_scaner.update()
    def input(self,key):
        self.game_scaner.input(key)
    def delete(self):
        self.game_scaner.delete()
    def replace(self,scene):
        self.game_scaner.delete()
        self.game_scaner=self.Scene(package=self.package+"/"+scene)
load=Text(text="loading...")
Title(text='Ark Game β 0.5 3/4')
def_system_data["game"]=Game(package=def_system_data["system_data"]["appdata"],scene="新的世界")
destroy(load)
app.run()