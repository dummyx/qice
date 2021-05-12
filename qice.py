import boto3
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit

import settings

def create_circuit(bits:int=8)->Circuit:
    circ = Circuit()
    for i in range(bits):
        circ.h(i)
    return circ

def qice(circ:Circuit)->int:
    device = AwsDevice(settings.device_arn)
    task = device.run(circ, (settings.s3_bucket,'qice'), poll_timeout_seconds=24*60*60, shots=1)
    result = task.result()
    counts = result.measurement_counts
    result_int = int(list(counts.keys())[0],2)
    return result_int

def qice_simulation(circ:Circuit)->int:
    local_sim = LocalSimulator()
    result = local_sim.run(circ, shots=1).result()
    counts = result.measurement_counts
    result_int = int(list(counts.keys())[0],2)
    return result_int

if __name__ == '__main__':
    res = qice(create_circuit())
    print(res)