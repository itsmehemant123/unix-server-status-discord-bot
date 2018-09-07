import discord
from datetime import datetime
from dateutil import tz
from discord.ext import commands
import psutil
import logging
import subprocess
from pynvml import *

class ServerStats:

    def __init__(self, bot):
        logging.basicConfig(level=logging.INFO)
        self.bot = bot
        self.to_zone = tz.gettz('America/Indianapolis')

    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx):
        usage = discord.Embed(title='Server Usage',
                              description='My Embed Content.', colour=0x00CC33, timestamp=datetime.now().astimezone(self.to_zone))
        
        usage.description = 'Both CPU and RAM readouts are the % used.\n\n'
        num_cpus = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent()
        virt_memory = psutil.virtual_memory()
        ram_usage = virt_memory[2]

        usage.add_field(name='CPU %', value=str(
            cpu_usage) + '% of ' + str(num_cpus) + ' cores', inline=True)
        usage.add_field(name='RAM %', value=str(
            ram_usage) + '% of 64GB', inline=True)

        if (cpu_usage > 80):
            usage.description += '‼️ High CPU usage'

        await ctx.send(embed=usage)

    @commands.command(pass_context=True, no_pm=True)
    async def users(self, ctx):
        usage = discord.Embed(title='Server Usage',
                              description='My Embed Content.', colour=0x00CC33, timestamp=datetime.now().astimezone(self.to_zone))

        usage.description = 'Logged in users:'
        logged_in_users = psutil.users()
        user_list = ''
        time_list = ''

        for user in logged_in_users:
            user_list += user[0] + '\n'
            time_list += datetime.fromtimestamp(user[3], self.to_zone).strftime('%Y-%m-%d %H:%M:%S') + '\n'
        
        usage.add_field(name='usernames', value=str(
            user_list), inline=True)

        usage.add_field(name='logged in since', value=str(
            time_list), inline=True)
        
        await ctx.send(embed=usage)

    @commands.command(pass_context=True, no_pm=True)
    async def gpuinfo(self, ctx):
        nvmlInit()
        
        deviceCount = nvmlDeviceGetCount()
        usage = discord.Embed(title='GPU Usage',
                              description='My Embed Content.', colour=0x00CC33, timestamp=datetime.now().astimezone(self.to_zone))

        status = ""

        for i in range(deviceCount):
            dHandle = nvmlDeviceGetHandleByIndex(i)

            gpuInfo = "*Device " + str(i) + "*\n"

            dName = nvmlDeviceGetName(dHandle).decode("utf-8")
            
            dUtil = nvmlDeviceGetUtilizationRates(dHandle) # gpu, memory
            gpuInfo += "**GPU Usage**: " + \
                str(dUtil.gpu) + "%\n"

            dMemInfo = nvmlDeviceGetMemoryInfo(dHandle) #total, free, used
            gpuInfo += "**Memory Usage**: " + \
                "{0:.2f}".format(dMemInfo.used * 100 / dMemInfo.total) + "%\n"
            

            dFanSpeed = nvmlDeviceGetFanSpeed(dHandle) # print with %
            gpuInfo += "**Fan Speed**: " + str(dFanSpeed) + "%"
            if (dFanSpeed > 85):
                gpuInfo += "🔥"
            gpuInfo += "\n"

            dPerfState = nvmlDeviceGetPerformanceState(dHandle)
            gpuInfo += "**Perf. State**: " + str(dPerfState) + "\n"
            
            dGPUTemps = nvmlDeviceGetTemperature(dHandle, NVML_TEMPERATURE_GPU) # prints in Celcius
            gpuInfo += "**Temperature**: " + str(dGPUTemps) + "C"
            if (dGPUTemps > 80):
                gpuInfo += "🔥"
            gpuInfo += "\n"

            dCurrentWattage = nvmlDeviceGetPowerUsage(dHandle) # divide by 1000 to get wattage
            dMaxWattage = nvmlDeviceGetEnforcedPowerLimit(dHandle) # same as above
            gpuInfo += "**Wattage**: " + \
                str(dCurrentWattage / 1000) + "W / " + \
                str(dMaxWattage / 1000) + "W"
            if ((dCurrentWattage / dMaxWattage) > 90):
                gpuInfo += "⚡️"
            gpuInfo += "\n"

            # dProcs = nvmlDeviceGetComputeRunningProcesses(dHandle)

            status += "*Device " + str(i) + "*: " + dName
            if (dUtil.gpu == 0 and int(dMemInfo.used * 100/dMemInfo.total) == 0):
                status += "✅\n"
            else:
                status += "❌\n"

            usage.add_field(name=dName, value=gpuInfo, inline=True)
        
        nvmlShutdown()

        usage.description = "Make sure to check that both GPU and Memory Utilization are 0 before running a task.\n\n ✅ Indicates free GPU.\n ❌ Indicates GPU being used, do not pick this GPU to run your script.\n\n" + status
        
        await ctx.send(embed=usage)

    def shutdown(self):
        nvmlShutdown()  

def setup(bot):
    bot.add_cog(ServerStats(bot))
