# Hyper-GPU

Ce repository présente un script Python permettant la gestion de paravirtualisation de processeur graphique NVIDIA.

La fonctionnalitée de copie des pilotes NVIDIA hôte vers la machine virtuelle ne fonctionne pas (d'après les tests). L'implémentation reste néanmoins dans le commit
pour ceux à qui cela pourrais fonctionner par magie.

Veuillez noter que cela ne peut que fonctionner sur Hyper-V, et il est fortement recommandé que vous ayez les prérequis suivants:

   - Microsoft Windows 10/8.1 Profesionnel ou Entreprise
   - La plateforme de virtualisation Hyper-V
   - Un processeur graphique NVIDIA avec au moins 2GB de mémoire vidéo
   - Un minimum de 12 GB de RAM
   - Un processeur avec la topologie minimum suivante:
   - Support de la virtualisation Intel VT-d/VT-x, ou AMD VI
   - 4 Cores
   - 4 Processeurs logiques ou plus

N'oubliez pas d'installer la dernière version disponible de Python pour Windows, et d'installer les modules inclus dans modules.txt avec PIP.

# Interface graphique du programme
![image](https://github.com/LThomas248/Hyper-GPU/assets/83450517/8a320602-7b54-4290-9ddf-b38413ac9a61)


# Séléction graphique des machines virtuelles Hyper-V
![image](https://github.com/LThomas248/Hyper-GPU/assets/83450517/c63b0e55-1f82-4f46-bd60-170b9c7c4130)


Veuillez comprendre que ce projet ne vient avec aucune garantie de fonction parfaite.

