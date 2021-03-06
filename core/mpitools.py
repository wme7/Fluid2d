from param import Param
from numpy import zeros,max,sum,array
from mpi4py import MPI

class Mpitools(Param):
    def __init__(self,param):
        self.list_param=['npx','npy','myrank']
        param.copy(self,self.list_param)

        self.nbproc = self.npx * self.npy


    def local_to_global(self, list_scalars):
        """ dict_scalars is a list of tuples
       [ (value,'sum'), (value,'max') ...] """
        
        nb = len(list_scalars)
        cst = zeros((nb,))

        for k in range(nb):
            cst[k] = list_scalars[k][0]


        if self.nbproc>1:
            cst_glo = array(MPI.COMM_WORLD.allgather(cst))
        
            for k in range(nb):
                ope = list_scalars[k][1]
                if ope=='max':
                    cst[k] = max(cst_glo[:,k])
                if ope=='sum':
                    cst[k] = sum(cst_glo[:,k])
        
        return cst
        
if __name__ == "__main__":
    
    p = Param()
    p.npx = 2
    p.npy = 2

    rank = MPI.COMM_WORLD.Get_rank()
    p.myrank = rank

    d=[(rank,'max'),(1,'sum'),(rank,'sum')]

    tool = Mpitools(p)

    r=tool.local_to_global(d)

    if rank==0:
        print('max(rank)=',r[0])
        print('sum(1)   =',r[1])
        print('sum(rank)=',r[2])

