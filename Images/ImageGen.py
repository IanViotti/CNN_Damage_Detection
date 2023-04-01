import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time


def GetFilePath(damageType):
    '''
    Get damage files based on damage type
    '''
    researchProjectPath = os.path.abspath(os.getcwd())
    if damageType == 'core':
        modePath = os.path.abspath(os.path.join(researchProjectPath, 'DataBase', 'DB_core_damage', 'core_damage'))
        damagePath = os.path.abspath(os.path.join(modePath, '..'))
    elif damageType == 'skin1':
        modePath = os.path.abspath(os.path.join(researchProjectPath, 'DataBase', 'DB_skin_damage_n_1', 'skin_damage_n_1'))
        damagePath = os.path.abspath(os.path.join(modePath, '..'))
    elif damageType == 'skin4':
        modePath = os.path.abspath(os.path.join(researchProjectPath, 'DataBase', 'DB_skin_damage_n_4', 'skin_damage_n_4'))
        damagePath = os.path.abspath(os.path.join(modePath, '..'))
    else:
        raise Exception(f'Insert a valid damage type (core, skin1, skin4).\'{damageType}\' is not valid.')

    return modePath, damagePath

def GetDamageParameter(damageNum, damagePath):
    '''
    Read the damage variables and return an array with it
    '''
    parameterFile = os.path.join(damagePath, 'Damage_variables.csv')
    damageParam = pd.read_csv(parameterFile)
    damageVariables = damageParam.iloc[damageNum-1].to_numpy()

    return damageVariables

def GetModeMatrix(damageNum, modeNum, modePath, damageType):
    '''
    Read mode file and reuturn a square matrix containing UZ for plotting
    '''
    filePath = os.path.join(modePath, f'{damageNum}_Mode{modeNum}.txt')
    damageDF = pd.read_csv(filePath, sep=r'\s+',  index_col=0, names=['NodeNum', 'X', 'Y', 'Z', 'UX', 'UY', 'UZ'],
                           skiprows=1).drop(['UX', 'UY'], axis=1)
    damageDF = damageDF.drop(damageDF[damageDF.Z != 0].index).drop(['Z'], axis=1)
    damageDF = damageDF.drop_duplicates(subset=['X', 'Y'], keep='last')
    if damageType == 'core':
        damageDF.drop(damageDF.head(len(damageDF) - 2401).index,inplace=True)
    damageDF = damageDF.sort_values(by=['Y','X'])
    modeUZ = damageDF['UZ'].to_numpy()
    modeUZ = np.split(modeUZ, np.sqrt(len(modeUZ)))
    
    return modeUZ

def SaveModeFig(modeMatrix, damageParameter, damageType, modeNum):
    '''
    Plot and save a mode figure with normalized values between -7 and 7
    '''
    pcm = mpl.colors.Normalize(vmin=-7, vmax=7)
    fig, ax = plt.subplots()
    ax.matshow(modeMatrix, norm=pcm, cmap='viridis')
    ax.axis('off')
    damageParameterStr = '_'.join(map(str, damageParameter.round(5))) # round value for naming image file
    imagePathName = os.path.join('ImageGeneration', 'Images', f'{damageType}_{damageParameterStr}_Mode{modeNum}.jpg')
    plt.savefig(imagePathName, bbox_inches='tight', pad_inches = 0)
    plt.close(fig)

def main(damageType, modes, damages):
    initialTime = time.time()

    modePath, damagePath = GetFilePath(damageType)

    for damageNum in damages:
        for modeNum in modes:
            damageParameter = GetDamageParameter(damageNum, damagePath)
            try:
                modeMatrix = GetModeMatrix(damageNum, modeNum, modePath, damageType)
            except:
                continue
            SaveModeFig(modeMatrix, damageParameter, damageType, modeNum)

            print(f'Saved Mode {modeNum} Damage {damageNum}. Elapsed time: {((time.time() - initialTime)/60):.2f}min') #Log
    
    print('\nFinished.')

if __name__ == '__main__':
    modes = np.arange(1,6,1)
    damages = np.arange(1,1001,1)
    damageType = 'skin4'
    main(damageType, modes, damages)
