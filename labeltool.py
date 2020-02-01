import glob, cv2, os
from shutil import copyfile

srcdir = '/Users/xianpf/Documents/children_face/srcImgs'
dstdir = '/Users/xianpf/Documents/children_face/labeledImgs'

fnames = glob.glob(srcdir+'/**', recursive=True)

for fn in fnames:
    if fn.endswith('.png'):
        # import pdb; pdb.set_trace()
        print('Processing image :', fn)
        if fn.endswith('ori.png'):
            continue
        else:
            dirname, fn_only = os.path.split(fn)
            fn_head = fn_only.split('.png')[0]
            new_dir = dirname.replace(srcdir, dstdir)
            new_dir_fnames = []
            if os.path.exists(new_dir):
                new_dir_fnames = glob.glob(new_dir+'/**', recursive=True)
                processed = False
                processed_name = ''
                for ndfn in new_dir_fnames:
                    if ndfn.startswith(os.path.join(new_dir, fn_head + '_TO_')):
                        processed = True
                        processed_name = os.path.basename(ndfn)
                # import pdb; pdb.set_trace()
                if processed:
                    print('该图片已处理过，从{}标注为{}'.format(fn_only, processed_name))
                    continue

            ori_img_fn = dirname + '/ori.png'
            ori_img = cv2.imread(ori_img_fn)
            ori_h, ori_w = ori_img.shape[0], ori_img.shape[1]
            target_h = 600
            target_w = round(target_h / ori_h * ori_w)
            ori_img_resized = cv2.resize(ori_img, (target_w, target_h))
            cv2.imshow('origin image', ori_img_resized)
            face_img = cv2.imread(fn)
            # cv2.putText(face_img, "foot ball", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('face image', face_img)
            cv2.waitKey(10)

            t_in_role = input('这是爸爸(1)/妈妈(2)还是孩子(3-9)?|按r刷新|按s同类处理  ')
            same_processed = False
            while not (same_processed or (t_in_role.isdigit() and 0 < int(t_in_role) < 10)):
                if t_in_role == 'r' or t_in_role == 'R':
                    print('刷新图片')
                    cv2.imshow('face image', face_img)
                    cv2.waitKey(10)
                elif t_in_role == 's' or t_in_role == 'S':
                    print('按照已处理的相同图片处理，本图短名为：'+fn_head)
                    same_processed = True
                else:
                    print('输入无效， 请重新输入。')
                t_in_role = input('这是爸爸(1)/妈妈(2)还是孩子(3-9)?|按r刷新|按s同类处理  ') if not same_processed else '0'
            if not same_processed:
                if int(t_in_role)>=3:
                    t_in_gender = input('这是男孩(1)还是女孩(2)?  ')
                    while not (t_in_gender.isdigit() and 0 < int(t_in_gender) < 3):
                        print('输入无效， 请重新输入。')
                        t_in_gender = input('这是男性(1)还是女性(2)?  ')
                else:
                    t_in_gender = t_in_role
                t_in_race = input('此人肤色为黄种人(1)/白种人(2)/黑人(3)还是棕色人种(4)?  ')
                while not (t_in_race.isdigit() and 0 < int(t_in_race) < 5):
                    print('输入无效， 请重新输入。')
                    t_in_race = input('此人肤色为黄种人(1)/白种人(2)/黑人(3)还是棕色人种(4)?  ')
                t_in_age = input('此孩子年龄介于0-3幼儿(1)/4-10儿童(2)还是11-15青年(3)?  ' \
                    if int(t_in_role)>=3 else '此家长年龄介于26-30年轻(1)/31-35中年(2)还是36-40老年(3)?  ')
                while not (t_in_age.isdigit() and 0 < int(t_in_age) < 4):
                    print('输入无效， 请重新输入。')
                    t_in_age = input('此孩子年龄介于0-3幼儿(1)/4-10儿童(2)还是11-15青年(3)?  ' \
                        if int(t_in_role)>3 else '此家长年龄介于26-30年轻(1)/31-35中年(2)还是36-40老年(3)?  ')
                t_in_emotion = input('此人表情为一般(1)/露齿笑(2)还是难过(3)?  ')
                while not (t_in_emotion.isdigit() and 0 < int(t_in_emotion) < 4):
                    print('输入无效， 请重新输入。')
                    t_in_emotion = input('此人表情为一般(1)/露齿笑(2)还是难过(3)?  ')
                t_in_glasses = input('此人戴(1)还是不戴(2)眼镜?  ')
                while not (t_in_glasses.isdigit() and 0 < int(t_in_glasses) < 3):
                    print('输入无效， 请重新输入。')
                    t_in_glasses = input('此人戴(1)还是不戴(2)眼镜?  ')
                t_in_moustache = input('此人留(1)还是不留(2)胡子?  ')
                while not (t_in_moustache.isdigit() and 0 < int(t_in_moustache) < 3):
                    print('输入无效， 请重新输入。')
                    t_in_moustache = input('此人留(1)还是不留(2)胡子?  ')

                descrip_str = '0'+t_in_role+t_in_gender+t_in_race+t_in_age+t_in_emotion+t_in_glasses+t_in_moustache
            else:
                ndfn_shortnames = [os.path.basename(ndfn).split('_TO_')[0] for ndfn in new_dir_fnames[1:]]
                sn_w_id = [os.path.basename(ndfn).split('_TO_')[0] +':'+ os.path.basename(ndfn).split('_TO_')[-1][:2] for ndfn in new_dir_fnames[1:]]
                ndids = [os.path.basename(ndfn).split('_TO_')[-1][:2] for ndfn in new_dir_fnames[1:]]
                ndids_unique = list(set(ndids))
                print('已处理的原图文件名有：', sn_w_id)
                t_in_same = input('请输入相同图片处理的原图文件短名:  ').replace('-', '_')
                same_fn = ''
                while t_in_same not in (ndfn_shortnames + ndids):
                # while t_in_same not in ndfn_shortnames:
                    print('没匹配到处理好的图片， 请重新输入。')
                    t_in_same = input('请输入相同图片处理的原图文件短名:  ').replace('-', '_')
                # import pdb; pdb.set_trace()
                same_fn = os.path.basename(new_dir_fnames[ndfn_shortnames.index(t_in_same)+1]) \
                    if '_' in t_in_same else os.path.basename(new_dir_fnames[ndids.index(t_in_same)+1])

                descrip_str = same_fn.split('.png')[0].split('_TO_')[1]
                # descrip_str = 
            print('此人的描述字符串为：', descrip_str)

            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_fn = fn_head + '_TO_' + descrip_str + '.png'


            t_in_sure = input('此人的描述字符串为：'+descrip_str+'｜确定无误?正确(y)重来(n)  ')
            while t_in_sure not in ['y', 'n']:
                print('输入无效， 请重新输入。')
                t_in_sure = input('此人的描述字符串为：'+descrip_str+'｜确定无误?正确(y)重来(n)  ')
            if t_in_sure == 'y':
                copyfile(fn, os.path.join(new_dir, new_fn))
            elif t_in_sure == 'n':
                print('操作已丢弃，重新来过。')
                fnames.insert(0, fn)
            else:
                import pdb; pdb.set_trace()

            # import pdb; pdb.set_trace()
