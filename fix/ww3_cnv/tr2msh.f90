      integer nm(3)
      open(10,file="hgrid.gr3")
      open(11,file="wwmbnd.gr3")
      open(20,file="hgrid.msh")
      open(21,file="OB.nml")
      read(10,*)
      read(10,*)ne,np
      write(20,*) "$MeshFormat"
      write(20,*) "2 0 8"
      write(20,*) "$EndMeshFormat"
      write(20,*) "$Nodes"
      write(20,*) np
      do i=1,np
        read(10,*)j,xtmp,ytmp,dp
        write(20,'(i8,2(1x,f14.8),1x,f10.3)')j,xtmp,ytmp,dp
      enddo !i

      write(20,*) "$EndNodes"
      write(20,*) "$Elements"
!     Swap read for open boundary
      do i=1,ne
         read(10,*)
      end do

!     Read Open boundary
      read(10,*) ntob
      read(10,*) ntop
      read(10,*) nob
!     Read from wwmbnd
      read(11,*)
      read(11,*)
      iobwwm=0
      do i=1,np
         read(11,*)j,xtmp,ytmp,dp
         if (dp.eq.2.) iobwwm=iobwwm+1
      end do
      nob=iobwwm
      write(20,*) ne+nob
      rewind(11)
      read(11,*)
      read(11,*)
!     Write OB
      ic0=0
      do i=1,np !nob
         read(11,*) j,xtmp,ytmp,dp
         if (dp.eq.2.) then
           jj=i
           ic0=ic0+1
           write(20,*) ic0,"15  2  0  0  ",jj
!     Format 
!     INBND_POINT(1)         =  217 1 F
           write(21,'(a,i3,a,i4,a)') "INBND_POINT(",ic0,")  = ",jj," 1 F"
         end if
      end do
!     Rewind and swap read for ele
      rewind(10)
      do i=1,np+2
         read(10,*)
      end do
!     Write ele
      do i=1,ne
        read(10,*)j,k,nm(1:k)
        if (k.eq.4) write(*,*) 'quads:',j
        write(20,'(i7,3i3,i7,i2,3i7)')j+nob,2,k,0,j,0,nm(1:k)
      enddo !i
      close(10)
      close(20)


      end

