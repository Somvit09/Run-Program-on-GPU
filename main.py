import time
import torch
import logging
import threading

from password_list import *


class RunProgramsOnGPU:
    def __init__(self, **kwargs):
        self.is_cuda_available = torch.cuda.is_available()
        self.no_of_gpus = torch.cuda.device_count()
        self.available_gpus = []
        self.current_device = None
        
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        
    def get_available_gpus(self):
        try:
            if self.is_cuda_available:
                for i in range(self.no_of_gpus):
                    gpu_name = torch.cuda.get_device_name(i)
                    self.available_gpus.append((i, gpu_name))
        except Exception as e:
            logging.exception(e)
         
    def check_gpu_usage(self):
        try:
            while True:
                if self.is_cuda_available:
                    logging.info("Checking GPU usage...")
                    self.current_device = torch.cuda.current_device()
                    logging.info(f"Current GPU: {torch.cuda.get_device_name(self.current_device)}")
                    total_memory = torch.cuda.get_device_properties(self.current_device).total_memory
                    allocated_memory = torch.cuda.memory_allocated(self.current_device)
                    cached_memory = torch.cuda.memory_reserved(self.current_device)
                    memory_usage_percentage = (allocated_memory / total_memory) * 100
                    
                    logging.info(f"Total Memory: {total_memory / 1e9:.2f} GB")
                    logging.info(f"Allocated Memory: {allocated_memory / 1e9:.2f} GB")
                    logging.info(f"Cached Memory: {cached_memory / 1e9:.2f} GB")
                    logging.info(f"Memory Usage Percentage: {memory_usage_percentage:.2f}%")
                    if KeyboardInterrupt:
                        break
                else:
                    logging.warning("CUDA is not available. GPU usage cannot be checked.")
                time.sleep(35)
        except Exception as e:
            logging.exception(e)  
        
    def run_with_gpu(self, function):
        try:
            while True:
                if self.is_cuda_available:
                    self.get_available_gpus()
                    if self.available_gpus:
                        logging.info("Available GPUs:")
                        [logging.info(f"GPU {gpu_index}: {gpu_name}") for gpu_index, gpu_name in self.available_gpus]  
                        try:
                            gpu_indices = ', '.join([str(i) for i in range(self.no_of_gpus)])
                            gpu_index = int(input(f"Enter the index number of the GPU you want to use (e.g., {gpu_indices}): "))
                            torch.cuda.set_device(gpu_index)
                            torch.set_default_tensor_type(torch.cuda.FloatTensor)
                            if callable(function):
                                function_thread = threading.Thread(target=function)
                                gpu_usage_thread = threading.Thread(target=self.check_gpu_usage)
                                function_thread.start()
                                gpu_usage_thread.start()
                                function_thread.join()
                                gpu_usage_thread.join()  
                            break
                        except KeyboardInterrupt:
                            break
                        except (ValueError, KeyError, RuntimeError, ModuleNotFoundError) as error:
                            raise error
                        except Exception as e:
                            raise e
                else:
                    logging.warning("CUDA is not available.")
        except threading.ThreadError as t:
            logging.exception(str(t))
        except (ValueError, KeyError, RuntimeError, ModuleNotFoundError) as v:
            logging.exception(v)
        except Exception as e:
            logging.exception(e)
            
            
            
s = RunProgramsOnGPU()
s.run_with_gpu(get_password_list_optimized)