#
# This kind of tests should go against the emulator the same way as against real hardware.#
# Well now at least this file goes against real hardware
#

import pytest
from lucipy import LUCIDAC, Circuit
from lucipy.simulator import remove_trailing
from fixture_circuits import sinus

@pytest.fixture
def hc():
    hc = LUCIDAC("tcp://192.168.150.229:5732")
    hc.reset_circuit()
    yield hc
    hc.sock.sock.close() # or similar

# tests the protocol and configuration readout
def test_set_circuit_for_cluster(hc):
    set_conf_cluster = sinus().generate(skip="/M1") # Test Hardware has no M1!)
    hc.set_circuit(set_conf_cluster)
    get_conf_cluster = hc.get_circuit()["config"]
           
    # canonicalize I block defaults:
    for i,v in enumerate(get_conf_cluster["/0"]["/I"]["outputs"]):
        if not v:
            get_conf_cluster["/0"]["/I"]["outputs"][i] = []
    
    # get rid of M1 block
    del get_conf_cluster["/0"]["/M1"]
            
    print(f"{set_conf_cluster["/0"]=}")
    print(f"{get_conf_cluster["/0"]=}")
    
    ## Differences are still in the U-block. Look carefully.
    ## Probably we have an old an unsuitable commit.
    
    assert set_conf_cluster["/0"] == get_conf_cluster["/0"]

# tests the protocol and configuration readout
def test_set_adc_channels(hc):
    c = Circuit()
    c.set_adc_channels([0,1,2])
    set_conf = c.generate(skip="/M1")  # Test Hardware has no M1!
    print(f"{set_conf=}")
    hc.set_config(set_conf)
    get_conf = hc.get_circuit()["config"]
    
    # canonicalize: Remove trailing "None"
    get_adc_channels = remove_trailing(get_conf["adc_channels"])    
    
    print(f"{get_conf=}")
    print(f"{get_adc_channels=}")
    assert get_adc_channels == c.adc_channels

def test_ramp(hc):
    # This circuit uses the constant giver for integrating over a constant
    
    ic = +1
    slope = -1
    t_final = 2
    expected_result = -t_final*slope - ic
    assert expected_result == +1

    ramp = Circuit()
    i = ramp.int()
    assert i.out == 0
    
    c = ramp.const()
    assert c.out == 14
    
    ramp.connect(c, i, weight=slope)
    ramp.set_ic(0, ic)
    
    channel = ramp.measure(i)
    
    conf = ramp.generate(skip="/M1")
    hc.set_circuit(conf)
    
    hc.set_daq(num_channels=2)
    hc.set_run(halt_on_overload=False, ic_time=200_000, op_time=200_000, no_streaming=True)

    run = hc.start_run()
    data = array(run.data())
    x_hw = data.T[channel]
    t_hw = linspace(0, 2, len(x_run))
    
    sim = Simulation(ramp)
    assert sim.constant[0] == slope
    assert all(sim.constant[1:] == 0)
    sim_data = sim.solve_ivp(2, dense_output=True)
    t_sim = t_hw
    x_sim = sim_data.sol(t_hw)[i.id]
    # instead of:
    # x_sim = sim_data.y[i.id]
    # t_sim = sim_data.t

    import numpy as np
    # Large tolerance mainly because of shitty non-streaming
    # data aquisition
    assert np.isclose(x_sim[-1], expected_result, atol=0.01)
    assert np.isclose(x_hw[-1],  expected_result, atol=0.2)
    
    assert np.allclose(x_sim, x_hw, atol=0.2)


# TESTs to add:
#
#
#  1) Very short runtime: daq
#  2) Very long runtime: daq