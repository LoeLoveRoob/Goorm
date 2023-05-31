# -*- coding: utf-8 -*-



from GoormAPI import GoormIDE
from GoormAPI import GoormResponse
from sys import argv
from time import sleep
from random import randint




goorm_session = GoormIDE(
    email= argv[1],
    password= argv[2]
)


if (goorm_session.Login()) == GoormResponse.Success:
    print("Login To Your Account SuccessFully !!!\n")
    container_name = argv[3]
    container_data = [i if (i["ProjectName"]) == container_name else None for i in (goorm_session.GetContainerList())][0]
    if container_data:
        print("Start Checking ...")
        while True:
            goorm_session.RunContainer(container_data["ProjectUID"])
            sleep(randint(300, 600))
    else:
        print(f"\n\nError : Container '{container_name}' Not Found !!!\n")
else:
    print("\n\nError : Invalid Email & Password !!!\n")

