'''
Created on Aug 7, 2016

@author: UNIST
'''

import logging

from opsupport_bpm.aco.aco_misc import random_generate_hg
from opsupport_bpm.util.print_hypergraph import write_hg_to_file,\
    print_hg_std_out_only
from opsupport_bpm.aco.evaluation import optimise
from opsupport_bpm.aco.evaluation import cleanup
from time import time

from opsupport_bpm.aco.aco_directed_hypergraph import aco_algorithm_norec


def do_one_run(io_param, aco_param, hg_gen_param):
    # set up working directory
    working_dir = io_param['working_dir']
    output_eval_dir = io_param['output_eval_dir']
    # all the pnml files in input_eval_dir will be evaluated
    input_eval_dir = io_param['input_eval_dir']
    
    
    
    # set up ACO params
    COL_NUM = aco_param['COL_NUM']
    COL_NUM_MAX = aco_param['COL_NUM_MAX']
    COL_NUM_STEP = aco_param['COL_NUM_STEP']
    ANT_NUM = aco_param['ANT_NUM']
    ANT_NUM_MAX = aco_param['ANT_NUM_MAX']
    ANT_NUM_STEP = aco_param['ANT_NUM_STEP']
    phero_tau = aco_param['phero_tau']
    W_UTILITY = aco_param['W_UTILITY']
    
    
    # setup hg generation params
    L_SIZE = hg_gen_param['level_size']
    B_SIZE_MIN = hg_gen_param['block_size_min']
    B_SIZE_MAX = hg_gen_param['block_size_max']
    
    # generate hg
    hg = random_generate_hg(L_SIZE, B_SIZE_MIN, B_SIZE_MAX)
    hg_gen_file_name = input_eval_dir + '/test_rewrite.hgr'
    write_hg_to_file(hg, hg_gen_file_name)
    
    # run optimisation
    #optimise(io_param, aco_param)
    
    start_time_aco = time()
    aco_result = aco_algorithm_norec(hg, ANT_NUM, COL_NUM, phero_tau, W_UTILITY)
    p_opt = aco_result[0]
    utility = aco_result[1]
    end_time_aco = time()
    aco_alg_time = end_time_aco - start_time_aco
    print_hg_std_out_only(p_opt)
    print("ACO optimisation took: {0}s".format(aco_alg_time))
    print("UTILITY: {0}".format(utility))
    
    

if __name__ == "__main__":
    
    # set working directory
    working_dir = "C://opsupport_bpm_files"
    output_eval_dir = working_dir+"/eval/output_files"
    
    io_param = {}
    io_param['working_dir'] = working_dir 
    io_param['output_eval_dir'] = working_dir+"/eval/output_files"
    io_param['input_eval_dir'] = working_dir+"/eval/input_files"
    io_param['log'] = output_eval_dir+"/logs/run.log"
    
    # cleanup output directory
    cleanup(output_eval_dir)
    
    # set logger
    log_file = io_param['log']
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=log_file,level=logging.WARNING)
    
    
    # set aco parameters
    aco_param = {}
    aco_param['COL_NUM'] = 5
    aco_param['COL_NUM_MAX'] = 10
    aco_param['COL_NUM_STEP'] = 5
    aco_param['ANT_NUM'] = 15
    aco_param['ANT_NUM_MAX'] = 47
    aco_param['ANT_NUM_STEP'] = 9
    aco_param['phero_tau'] = 0.5
    W_UTILITY = {'cost' : 1.0, 'avail' : 0.0, 'qual' : 0.0, 'time' : 0.0}
    aco_param['W_UTILITY'] = W_UTILITY
    
    # set up hg gen params
    hg_gen_param = {}
    hg_gen_param['level_size'] = 3000
    hg_gen_param['block_size_min'] = 10
    hg_gen_param['block_size_max'] = 18
    
    do_one_run(io_param, aco_param, hg_gen_param)
    