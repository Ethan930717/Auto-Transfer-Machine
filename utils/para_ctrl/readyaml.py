import os
import yaml
from loguru import logger
from AutoTransferMachine.utils.getinfo.makeyaml import mkyaml

def readyaml(file):
    newfile=file+'.bak'
    logger.info('正在读取yaml...')
    f=open(file, encoding='utf-8')
    audata = yaml.load(f, Loader=yaml.FullLoader)
    mkyaml(audata)
    try:
        if (len(audata)<1):
            logger.warning('配置文件'+file+'数据少于一行，判断为数据缺失，已自动使用备份配置文件'+newfile)
            if os.path.exists(newfile):
                f=open(newfile, encoding='utf-8')
                audata = yaml.load(f, Loader=yaml.FullLoader)
            else:
                raise ValueError('配置文件'+file+'数据少于两行，判断为数据缺失，且未找到备份配置文件'+newfile+'请检查配置文件')

    except:
        logger.warning('配置文件'+file+'数据缺失，已自动使用备份配置文件'+newfile)
        f=open(newfile, encoding='utf-8')
        audata = yaml.load(f, Loader=yaml.FullLoader)

    f.close()
    logger.info('读取yaml完毕')
    #au_data['yaml_path']=file
    newfile=file+'.bak'
    write_yaml(audata,newfile)
    print(audata)
    return audata
    
def write_yaml(au_data,file=''):
    mod =''
    if file=='' and 'yaml_path' in au_data:
        file=au_data.pop('yaml_path')
    if 'mod' in au_data    :
        mod =au_data.pop('mod')
    if file=='':
        logger.error('未找到yaml文件信息,无法写入文件')
        raise ValueError ('未找到yaml文件信息,无法写入文件')

    logger.info('正在更新yaml中，请勿中途终止程序。如果特殊原因终止程序导致yaml文件内容丢失，请前往au.yaml.bak文件内容中找回')
    f=open(file, "w", encoding='utf-8')
    f.write(yaml.dump(au_data, allow_unicode=True, sort_keys=False))
    f.close()
    logger.info('更新yaml完毕')

    if not file=='' and not '.bak' in file:
        au_data['yaml_path']=file
    if not mod=='':
        au_data['mod']=mod
