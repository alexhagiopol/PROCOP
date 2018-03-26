def st_in(m1in,mm1in):
    f,fm,ai,bi = ([] for ki in range(4))
    m = len(mm10)
    for i in range(m):
        f.append(m1in[i]/(1-m1in[i]))
        fm.append(mm1in[i]/(1-mm1in[i]))
        ai.append(pow(fm[i],2)/f[i])
        bi.append(fm[i]*(1/f[i]-1))
    return ai,bi
def meth_knn():
   a,b,p11,p21,p12,p22,p13,p23,r1nn,r2nn,fnn,p1,p2,f12,diff,fcsso,r1sso,r2sso = ([] for kknn in range(18))
   in_dtknn = st_in(m1,mm10)
   a = in_dtknn[0]
   b = in_dtknn[1]
   ll = 0
   sso = 0
   err = 0.0001
   n = len(mm10)
   if len(mm10)==3:
       pp11 = (b[1]-b[2])/(a[2]-a[1])
       pp21 = (a[2]*b[1]-a[1]*b[2])/(a[2]-a[1])
       pp12 = (b[1]-b[3])/(a[3]-a[1])
       pp22 = (a[3]*b[1]-a[1]*b[3])/(a[3]-a[1])
       pp13 = (b[2]-b[3])/(a[3]-a[2])
       pp23 = (a[3]*b[2]-a[2]*b[3])/(a[3]-a[2])      
       r1knn = (pp11+pp12+pp13)/3
       r2knn = (pp21+pp22+pp23)/3
   else:
       book = xlwt.Workbook(encoding="utf-8")
       sh = book.add_sheet('Reactivity_Ratios')
       for i in range(n-2):
           for j in range(i+1,n-1):
               for s in range(j+1,n):
                   p11.append((b[i]-b[j])/(a[j]-a[i]))
                   p21.append((a[j]*b[i]-a[i]*b[j])/(a[j]-a[i]))
                   p12.append((b[i]-b[s])/(a[s]-a[i]))
                   p22.append((a[s]*b[i]-a[i]*b[s])/(a[s]-a[i]))
                   p13.append((b[s]-b[j])/(a[j]-a[s]))
                   p23.append((a[j]*b[s]-a[s]*b[j])/(a[j]-a[s]))
                   sh.write(ll+1,1,"{:10.4f}".format(p11[ll]))
                   sh.write(ll+1,2,"{:10.4f}".format(p21[ll]))
                   sh.write(ll+1,3,"{:10.4f}".format(p12[ll]))
                   sh.write(ll+1,4,"{:10.4f}".format(p22[ll]))
                   sh.write(ll+1,5,"{:10.4f}".format(p13[ll]))
                   sh.write(ll+1,6,"{:10.4f}".format(p23[ll]))
                   p11cen = (p11[ll]+p12[ll]+p13[ll])/3
                   p22cen = (p21[ll]+p22[ll]+p23[ll])/3
                   if p11cen < 0:
                       p11cen = 0.0001
                   if p22cen < 0:
                       p22cen = 0.0001
                   r1nn.append(p11cen)
                   r2nn.append(p22cen)
                   sh.write(ll+1,10,"{:10.4f}".format(r1nn[ll]))
                   sh.write(ll+1,11,"{:10.4f}".format(r2nn[ll]))
                   m1cnn = conversion(r1nn[ll],r2nn[ll])
                   fnn.append(fischer(m1cnn,r1nn[ll],r2nn[ll]))
                   ll += 1
       for i in range(ll,0,-1):
           for j in range(0,ll-1):
               if fnn[j] > fnn [j+1]:
                   fint = fnn[j]
                   r1int = r1nn[j]
                   r2int = r2nn[j]
                   fnn[j] = fnn[j+1]
                   r1nn[j] = r1nn[j+1]
                   r2nn[j] = r2nn[j+1]
                   fnn[j+1] = fint
                   r1nn[j+1] = r1int
                   r2nn[j+1] = r2int
       conf = False
       count = 0
       n3=ll
       while not conf:
           ll = 0
           del p1[:]
           del p2[:]
           for i in range(n3-2):
               for j in range(i+1,n3-1):
                   for ss in range(j+1,n3):
                       p1cen = (r1nn[i]+r1nn[j]+r1nn[ss])/3
                       p2cen = (r2nn[i]+r2nn[j]+r2nn[ss])/3
                       if p1cen < 0:
                           p1cen = 0.0001
                       if p2cen < 0:
                           p2cen = 0.0001
                       p1.append(p1cen)
                       p2.append(p2cen)
                       m1cpnn = conversion(p1[ll],p2[ll])
                       f12.append(fischer(m1cpnn,p1[ll],p2[ll]))
                       sh.write(ll+1,14,"{:10.4f}".format(p1[ll]))
                       sh.write(ll+1,15,"{:10.4f}".format(p2[ll]))
                       sh.write(ll+1,16,"{:10.4f}".format(f12[ll]))
                       ll += 1
           for i in range(ll,0,-1):
               for j in range(0,ll-1):
                   if f12[j] > f12[j+1]:
                       fint = f12[j]
                       p1int = p1[j]
                       p2int = p2[j]
                       f12[j] = f12[j+1]
                       p1[j] = p1[j+1]
                       p2[j] = p2[j+1]
                       f12[j+1] = fint
                       p1[j+1] = p1int
                       p2[j+1] = p2int
           for s in range(0,n):
               m1cp0 = conversion(p1[0],p2[0])
               diff.append(mayo_lewis(m1cp0[s],p1[0],p2[0])-m1[s])
           devstd = stat.stdev(diff)
           count += 1
           if count > 100:
               fcsso.append(f12[0])
               r1sso.append(p1[0])
               r2sso.append(p2[0])
               sso += 1
               err = err + 0.00005*sso
               count = 0
           if devstd < 0.1:
               r2knn = p2[0]
               r1knn = p1[0]
               conf = True
   fknn = fischer(mm10,r1knn,r2knn)
   m1cknn = conversion(r1knn,r2knn)
   fknnc = fischer(m1cknn,r1knn,r2knn)
   book.save('PBPMA-NVP nou.xls')
   if (r1knn < 1) and (r2knn < 1):
        azknn = azeotrop(r1knn,r2knn)
   else:
       azknn = 0
   return r1knn, r2knn, fknn, fknnc, azknn

    res_knn = meth_knn()
    print('kNN ',"{:10.4f}".format(res_knn[0]),"{:10.4f}".format(res_knn[1]),"{:10.4f}".format(res_knn[2]), "{:11.4f}".format(res_knn[3]),"{:10.4f}".format(res_knn[4]))
