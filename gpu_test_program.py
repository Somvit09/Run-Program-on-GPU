import torch
from password_list import get_password_list_optimized

print("Is CUDA available: ", torch.cuda.is_available())
print("Num GPUs Available: ", torch.cuda.device_count())

def get_available_gpus():
    try:
        available_gpus = []
        num_gpus = torch.cuda.device_count()
        for i in range(num_gpus):
            gpu_name = torch.cuda.get_device_name(i)
            available_gpus.append((i, gpu_name))
        return available_gpus
    except Exception as e:
        raise e



def check_gpu_usage():
    try:
        if torch.cuda.is_available():
            print("Checking GPU usage...")
            current_device = torch.cuda.current_device()
            
            print(f"Current GPU: {torch.cuda.get_device_name(current_device)}")
            
            total_memory = torch.cuda.get_device_properties(current_device).total_memory
            allocated_memory = torch.cuda.memory_allocated(current_device)
            cached_memory = torch.cuda.memory_reserved(current_device)
            memory_usage_percentage = (allocated_memory / total_memory) * 100
            
            print(f"Total Memory: {total_memory / 1e9:.2f} GB")
            print(f"Allocated Memory: {allocated_memory / 1e9:.2f} GB")
            print(f"Cached Memory: {cached_memory / 1e9:.2f} GB")
            print(f"Memory Usage Percentage: {memory_usage_percentage:.2f}%")
        else:
            print("CUDA is not available. GPU usage cannot be checked.")
    except Exception as e:
        raise e
        
        
def run_with_gpu(function):
    try:
        while True:
            if torch.cuda.is_available():
                available_gpus = get_available_gpus()
                if available_gpus:
                    print("Available GPUs:")
                    [print(f"GPU {gpu_index}: {gpu_name}") for gpu_index, gpu_name in available_gpus]  
                    try:
                        gpu_index = int(input("Enter the index number of the GPU you want to use (e.g., 0, 1, ...): "))
                        torch.cuda.set_device(gpu_index)
                        torch.set_default_tensor_type(torch.cuda.FloatTensor)
                        function()
                        break
                    except (ValueError, KeyError, RuntimeError, ModuleNotFoundError) as error:
                        raise error
                    except Exception as e:
                        raise e
            else:
                print("CUDA is not available.")
    except (ValueError, KeyError, RuntimeError, ModuleNotFoundError) as v:
        print(f"error: {v}")
    except Exception as e:
        print(f"error: {e}")

# Your computations here will now default to using the GPU if available
run_with_gpu(get_password_list_optimized)
check_gpu_usage()
