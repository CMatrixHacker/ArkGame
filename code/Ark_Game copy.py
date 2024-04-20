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
user_profile={"bag":False,"bag_open":True,"Hand_Block":None,"Hand_ID":-1,"up":False,'en':True,'HandBlock':0,'page':"Index","careful":"Main","game":None,'run_Block':None,"block_time":-1}
user_entity={}
resource_bag_block_dict={}
resource_block_time_dict={}
resource_texture_dict={}
def_const_num={}
def_package_path="./package"
def_json_data=json.load(open(def_package_path+"/config.json",'r'))
def_const_num["max_time"]=def_json_data["max"]
def_const_num["HP"]=def_json_data["HP"]
def_block_postion={}
def_bag_list=[]
user_profile["HP"]=def_json_data["HP"]
user_profile["scale"]=def_json_data["scale"]
'''以下代码为对系统的定义'''
for i in range(0,50): 
    resource_bag_block_dict[i]=None
    def_bag_list.append(0)
def ToAbs(path,mount="."):
    return os.path.abspath(os.path.join(mount, path))
def Tailor(json_data,Dict_Block,Dict_Block_time):
    img=Image.open(ToAbs(def_json_data["load_texture"],mount=ToAbs(def_package_path)))
    idx=0
    break_flag=False
    tmp_list_key=list(json_data["texture"].keys())
    tmp_list_value=list(json_data["texture"].values())
    for i in range(0,json_data["y"]*json_data["w"],json_data["h"]):
        if break_flag:
            break
        for j in range(0,json_data["x"]*json_data["h"],json_data["w"]):
            CropFileSave(ToAbs(def_json_data["load_texture"],mount=ToAbs(def_package_path)) ,Crop_data=[j,i,json_data["h"],json_data["w"],const_TMP_PATH,json_data["load_texture"]+str(i/json_data["h"])+"_"+str(j/json_data["w"])])
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
    if user_profile["game"]!=None:
        if key=="left mouse down" and user_profile["run_Block"]:
            user_profile["block_time"]=user_profile["time"]
def input_up(key, is_raw=False):
    print(key)
    if user_profile["game"]!=None:
        if key=="left mouse up" and user_profile["run_Block"]:
            if user_profile["block_time"]>=user_profile["run_Block"].block_time:
                destroy(user_profile["run_Block"])
            user_profile["block_time"]=-1
def input(key):
    global user_OccupyMouse
    if key.isdigit():
        user_profile['HandBlock']=int(key)-1
        if key=='0':
            user_profile['HandBlock']=9
    if key=="escape" and not(user_profile["bag"]):
            window.minimized=False
            player.enabled=not(player.enabled)
            mouse.visible = not(mouse.visible)
            user_OccupyMouse=not(user_OccupyMouse)  
            window.minimized=True
def update():
    global user_OccupyMouse,user_profile,user_HandBlock,resource_bag_block_dict
    if not user_profile["en"]:
        user_profile["game"].delete()
        exit()
    user_profile['fps']=window.fps_counter.text
    # print(user_profile["fps"])
    user_profile["time"]=time.time()
    user_HandBlock=IndexToValue(user_profile["HandBlock"],resource_bag_block_dict)
    if DeathVerdict(player.position,user_profile["HP"]):
        if(def_json_data["rebirth"]=="True"):
            user_profile["HP"]=def_const_num["HP"]
            player.position=(0,2,0)
    if user_OccupyMouse :
        def_const_num["rotation"]=player.rotation
    else :
        player.rotation=def_const_num["rotation"]
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
            elif def_bag_list[bag_value.index(self.texture)]<64:
                def_bag_list[bag_value.index(self.texture)]+=1
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
                    def_bag_list[bag_value.index(None)]+=1
                    resource_bag_block_dict[bag_value.index(None)]=self.texture
                    destroy(self)
                    break
            return 
    def update(self):
        self.rotation_y+=2
        if not self.intersects().hit:
            self.y-=0.5
        if self.intersects():
            if self.intersects().hit and not self.intersects(player).hit and type(self.intersects().entity)!=type(self):
                self.y+=0.5
                if self.y>self.init_y:
                    self.y=self.init_y-0.5
        if self.intersects(player).hit: 
            self.PickUp()
        if self.intersects(user_entity["sky"]).hit:
            destroy(self)      
class Block(Button):
    block_time=0
    global resource_block_time_dict
    def __init__(self,position=(0,0,0),texture=user_HandBlock):
            def_bag_list[user_profile['HandBlock']]-=1
            if def_bag_list[user_profile['HandBlock']]<0:
                def_bag_list[user_profile['HandBlock']]=0
            global def_block_postion,resource_block_time_dict,resource_texture_dict
            super().__init__(parent=scene,position=position,model="cube",highlight_color=color.gray,color=color.white,texture=texture,origin_y=0.5,collider='box')
            self.block_time=resource_block_time_dict[FindKeyByValue(texture,resource_texture_dict)]
    def input_down(self,key):
        if self.hovered and user_OccupyMouse:
            if key=="right mouse down" and user_HandBlock is not None:
                Block(position=self.position+mouse.normal,texture=user_HandBlock)
            elif key=="left mouse down":
                user_profile["run_Block"]=self
    def update(self):
        if user_profile["run_Block"]==self:
            if not self.hovered:
                user_profile["run_Block"]=None
        else:
            pass
class Backpack():
    class cell(Entity):
        idx=0
        entity=None
        text=None
        def __init__(self,position=(0,0),index=0):
            self.backdrop=Entity(position=position,model="cube",parent=camera.ui,scale=(0.1,0.1),color=(0,0,0.5,0.33),z=6)
            super().__init__(position=position,model="cube",parent=camera.ui,scale=(0.09,0.09),texture=IndexToValue(index,resource_bag_block_dict),z=5)
            global user_HandBlock,def_bag_list
            self.idx=index
            self.text=Text(text=str(def_bag_list[self.idx]),position=self.position+(0.02,-0.02),color=color.white,parent=camera.ui)
            self.id=Text(text=str((self.idx+1)%10),position=self.position+(0,-0.05),color=color.white,parent=camera.ui)
            self.backdrop.color=color.gray
        def update(self):
            self.text.z=4
            self.z=5
            if user_profile["Hand_ID"]==self.idx:
                self.texture=None;self.text.text=""
            else:
                self.text.text=str(def_bag_list[self.idx])
                if user_profile["HandBlock"]==self.idx:
                    self.backdrop.color=color.yellow
                else:
                    self.backdrop.color=color.gray
            self.texture=IndexToValue(self.idx,resource_bag_block_dict)
        def input(self,key):
            if key=="q" and user_profile["HandBlock"]==self.idx:
                pos=player.forward*2+player.position
                if def_bag_list[self.idx]>0:
                    Falling(position=pos+(0,0.3,0),texture=resource_bag_block_dict[self.idx])
                    def_bag_list[self.idx]-=1
    def __init__(self):
        global resource_bag_block_dict
        j=0
        for i in range(-5,5,1):
            self.cell(position=((i/10)+0.05,-0.42),index=j)  
            j+=1
class Bag(Entity):      
    entity=None
    class Hand_Block(Entity):
        text=None
        def __init__(self):
            super().__init__(texture=None,position=(1,1),z=1,parent=camera.ui,model="cube",scale=(0.045,0.045),Z=10)
            self.text=Text(text=str(def_bag_list[0]), position=self.position+(-0.001,0.001), color=color.white,parent=camera.ui,Z=1)
            self.text.visible=False
            self.visible=False
        def update(self):
            global resource_bag_block_dict,user_profile
            if user_profile["Hand_ID"]!=-1 and IndexToValue(user_profile["Hand_ID"],resource_bag_block_dict)!=None:
                self.visible=True
                self.text.visible=True
                self.text.position=self.position+(-0.001,0,-1)
                self.position=mouse.position
                self.texture=IndexToValue(user_profile["Hand_ID"],resource_bag_block_dict)
                self.text.text=def_bag_list[user_profile["Hand_ID"]]
            else:
                self.visible=False
                self.text.visible=False
                self.position=(1,1)
    class cell(Button):
        idx=0
        Hovered=False
        text=None
        mov=False
        entity=None
        def __init__(self,position=(0,0),index=0,parent=camera.ui):
            self.backdrop=Entity(position=position,model="cube",parent=parent,scale=(0.05,0.05),color=color.gray,z=4)
            textures=IndexToValue(index,resource_bag_block_dict)
            global def_bag_list
            super().__init__(position=position,model="cube",parent=camera.ui,color=color.white,scale=(0.045,0.045),texture=IndexToValue(index,resource_bag_block_dict),collider='box')
            self.text=Text(text=str(def_bag_list[self.idx]), position=position+(-0.001,0), color=color.white,parent=camera.ui)
            global user_HandBlock

            self.idx=index;self.backdrop.color=color.gray;self.backdrop.visible= False;self.visible=False;self.text.visible=False
        def input(self,key):
            global user_profile
            if self.Hovered and self.visible:
                if key=="left mouse down" and user_profile["Hand_ID"]==-1:
                    user_profile["Hand_ID"]=self.idx
                    user_profile["up"]=False
                    self.mov=True
                #以下代码用于防抖
                if key=="left mouse up" and user_profile["Hand_ID"]!=-1:
                    user_profile["up"]=True
                if key=="left mouse down" and user_profile["Hand_ID"]!=-1:
                    if user_profile["Hand_ID"]==self.idx and user_profile["up"]:
                        user_profile["Hand_ID"]=-1
                        self.mov=False
                    else:
                            tmp=resource_bag_block_dict[IndexToKey(self.idx,resource_bag_block_dict)]
                            resource_bag_block_dict[IndexToKey(self.idx,resource_bag_block_dict)]=resource_bag_block_dict[IndexToKey(user_profile["Hand_ID"],resource_bag_block_dict)]
                            resource_bag_block_dict[IndexToKey(user_profile["Hand_ID"],resource_bag_block_dict)]=tmp
                            tmp_1=def_bag_list[self.idx]
                            def_bag_list[self.idx]=def_bag_list[user_profile["Hand_ID"]]
                            def_bag_list[user_profile["Hand_ID"]]=tmp_1
            if key=="escape" and not user_profile["bag_open"]:
                self.backdrop.visible=not(self.backdrop.visible) ; self.visible=not(self.visible) ; self.text.visible=not(self.text.visible)
            if key=="e":
                self.backdrop.visible=not(self.backdrop.visible) ; self.visible=not(self.visible) ; self.text.visible=not(self.text.visible)
        def update(self): 
            global resource_bag_block_dict,user_profile
            if def_bag_list[self.idx]==0:
                resource_bag_block_dict[self.idx]=None
            if self.hovered:
                self.Hovered=True
            if not self.hovered:
                self.Hovered=False
            if not self.visible:
                self.mov=False
            self.texture=IndexToValue(self.idx,resource_bag_block_dict)
            if self.texture==None:
                def_bag_list[self.idx]=0
                self.text.text=""
            self.backdrop.z=7;self.z=3
            if def_bag_list[self.idx]==0:
                resource_bag_block_dict[self.idx]==None
            if self.mov == True:
                self.texture=None;self.text.text=""
                user_profile["Hand_Block"]=self
            else:
                self.texture=IndexToValue(self.idx,resource_bag_block_dict)
                if def_bag_list[self.idx]!=0:
                    self.text.text=def_bag_list[self.idx]
    def __init__(self):
        super().__init__(model="cube", parent=camera.ui, scale=(0.5, 0.55), color=(0, 0, 0), position=(0, 0),z=100)
        layer=-10
        self.visible=False
        idx=0
        Hand=self.Hand_Block()
        for j in range(-5,5,1):
            self.cell(position=((j/20)+0.025,-0.25),index=idx)
            idx+=1
        for i in range(1,5,1):
            for j in range(-5,5,1):
                self.cell(position=((j/20)+0.025,-0.22+(i/20)),index=idx)
                idx+=1
    def input(self,key):
        global user_OccupyMouse
        if key=="escape" and not user_profile["bag_open"]:
            user_profile["bag_open"]=True
        if (key == "e") and (user_OccupyMouse and not user_profile["bag"] or not user_OccupyMouse and user_profile["bag"]):
                self.visible=not(self.visible)
                player.enabled=not(player.enabled)
                user_profile["bag"]=not(user_profile["bag"])
                mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse) 
        if key == "escape" and not user_OccupyMouse and user_profile["bag"]:
            player.enabled=True
            self.visible=False;user_profile["bag"]=False;user_profile["bag_open"]=False
            mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse)
        if key == "e" and not user_OccupyMouse and not user_profile["bag"]:
            self.visible=not(self.visible)
            player.enabled=not(player.enabled)
            openBag=not(openBag)
            user_profile["bag_open"]=user_profile["bag"]=not(user_profile["bag"])
            mouse.visible = not(mouse.visible) ; user_OccupyMouse=not(user_OccupyMouse)
    def update(self):
        global user_profile
        if not self.visible:
            user_profile["Hand_ID"]=-1
class Sky(Entity):
    def __init__(self):
        global resource_texture_dict,user_profile
        super().__init__(parent=scene,model="sphere",scale=user_profile["scale"],texture=resource_texture_dict["sky"],double_sided=True,position=(0,0,0))
class Title(Entity):    
    exit_button=None
    minimize=None
    maximize=None
    def __init__(self,**kwargs):
        window.fps_counter.visible = False;window.collider_counter.visible = False;window.entity_counter.visible = False;window.exit_button.enabled=False;window.fullscreen=False;window.minimized=False
        text=Text(text=kwargs['text'],position=(-0.1,0.5),parent=camera.ui,z=3)
        text.position=(-1*(float(text.width)/2),0.5,0)
        super().__init__(model='cube',position=(0,0.5),parent=camera.ui,scale=(2,0.06),color=color.gray,z=4)
        self.exit_button=Button(model="sphere",text='X',parent=camera.ui,scale=(0.03,0.03),position=(0.873,0.485),z=2,color=color.red,text_color=color.black)
        self.maximize=Button(model="sphere",text='O',parent=camera.ui,scale=(0.03,0.03),position=(0.843,0.485),z=2,color=color.green,text_color=color.black)
        self.minimize=Button(model="sphere",text='_',parent=camera.ui,scale=(0.03,0.03),position=(0.813,0.485),z=2,color=color.yellow,text_color=color.black)
    def input(self,key):
        if self.minimize.hovered and key=='left mouse down':
            global user_OccupyMouse
            window.minimized=True
            player.enabled=not(player.enabled)
            player.enabled=not(player.enabled)
            window.minimized=False
        elif self.maximize.hovered and key=='left mouse down':
            window.minimized=False
            window.fullscreen=not(window.fullscreen)
            window.minimized=True
        elif self.exit_button.hovered and key=='left mouse down':
            global user_profile
            user_profile['en']=False
            print("正在通知所有进程关闭")
        else :
            window.minimized=False
class Game():
    class Quest(Thread):
        def __init__(self):
            super().__init__()
            print("start")
        def run(self):
            while user_profile["en"]:
                print("正在执行刷新任务")
                time.sleep(0.1)
    class Options(Entity):
        def __init__(self):
            super().__init__(model="cube",scale=(5,5),parent=camera.ui,position=(0,0),color=Color(0, 0, 0, 0.75),z=5)
            self.visible = False
        def input(self,key):
            self.visible = mouse.visible
    def __init__(self,**kwargs):
        user_profile["page"]="Game"
        global resource_texture_dict,resource_block_time_dict,player,user_entity
        def_json_data=json.load(open(kwargs['package']+"/config.json",'r'))
        print(def_json_data["seed"])
        player.enabled=True
        Tailor(def_json_data,resource_texture_dict,resource_block_time_dict)
        nosie=PerlinNoise(octaves=2.5,seed=def_json_data["seed"])
        scale = 24
        for z in range(-20,20):
            for x in range(-20,10):
                user_HandBlock=resource_texture_dict["bedrock"]
                i=int(nosie([x/scale,z/scale])*10)
                Block(position=(x,i,z),texture=resource_texture_dict["dirt"])
                for y in range(-2,i):
                    Block(position=(x,y,z),texture=resource_texture_dict["dirt"])
        user_entity["backpack"]=Backpack()
        user_entity["bag"]=Bag()
        user_entity["sky"]=Sky()
        user_entity["Options"]=self.Options()
        quest=self.Quest()
        quest.start()
        for i in range(0,50):
            resource_bag_block_dict[i]=None
    def delete(self):
        global user_profile
        user_profile["page"]="Index"
        user_profile["careful"]="Map"
        destroy(user_entity["bag"]);destroy(user_entity["sky"]);destroy(user_entity["Options"])
        del user_entity["backpack"]
        print("删除完成.....")
load=Text(text="loading...")
Tailor(def_json_data,resource_texture_dict,resource_block_time_dict)
player=FirstPersonController(collider="box")
Title(text='Ark Game β 0.5')
user_profile["game"]=Game(package="./package")
destroy(load)
app.run()
