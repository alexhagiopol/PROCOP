import math, random as ran, statistics as stat, xlwt
mm1,mm10,m1,conv,r1i,r2i,fi,mw,rr = ([] for k0 in range(9))

def read_data():
    mm1_str, m1_str, conv_str = ([] for k02 in range(3))
    f_nme = open('DataIn.dat','r')
    val_lines = f_nme.readlines()
    f_nme.close()
    for jj in range(2):
        mw.append(float(val_lines[jj]))
    m = int(val_lines[2])
    for i in range(m):
        mm1.append(float(val_lines[3*i+3]))
        mm10.append(float(val_lines[3*i+3]))
        m1.append(float(val_lines[3*i+4]))
        conv.append(float(val_lines[3*i+5]))
    print('      M1         m1        Yield ')
    for j in range(m):
        print("{:10.4f}".format(mm1[j]),"{:10.4f}".format(m1[j]),"{:10.4f}".format(conv[j]))
    return

def mayo_lewis(mm1ml,r1ml,r2ml):
    ml =(r1ml*pow(mm1ml,2)+mm1ml*(1-mm1ml))/(mm1ml*(1-mm1ml)+r2ml*pow(1-mm1ml,2))
    m1clc = ml/(1+ml)
    return m1clc

def lewis_mayo(mm2ml,r1ml,r2ml):
    ml =(r1ml*pow(mm2ml,2)+mm2ml*(1-mm2ml))/(mm2ml*(1-mm2ml)+r2ml*pow(1-mm2ml,2))
    m2clc = 1/(1+ml)
    return m2clc

def fischer(m1fis,r1fis,r2fis):
    m1clc = []
    m = len(mm10)
    sfis = 0
    for i in range(m):
        m1clc.append(mayo_lewis(m1fis[i],r1fis,r2fis))
        sfis += pow(m1clc[i]-m1[i],2)
    fis = 1000*math.sqrt(sfis/(m-2))
    return fis

def azeotrop(r1az,r2az):
    a = (r2az-1)/(r1az-1)
    azeo = a/(1+a)
    return azeo

def conversion(r1c,r2c):
    w10,w20,mm1cnv = ([] for kcnv in range(3))
    m = len(mm10)
    for i in range(m):
        w10.append(((mw[0]*mm10[i])/(mw[1]*(1-mm10[i])))/(1+(mw[0]*mm10[i])/(mw[1]*(1-mm10[i]))))
        w20.append((1)/(1+((mw[0]*mm10[i])/(mw[1]*(1-mm10[i])))))
    book = xlwt.Workbook(encoding="utf-8")
    sh = book.add_sheet('Conversion Data')
    ss = 0
    for i in range(m):
        mm1c = mm1[i]
        mm = int(1000*conv[i])
        for j in range(mm+1):
            m1clc = mayo_lewis(mm1c,r1c,r2c)
            m2clc = lewis_mayo(mm1c,r1c,r2c)
            w1 = m1clc*mw[0]/(mw[0]+mw[1])
            w2 = m2clc*mw[1]/(mw[0]+mw[1])
            cv = 0.001*j
            m1kw = (w10[i]-cv*w1)/(1-cv)
            m2kw = (w20[i]-cv*w2)/(1-cv)
            m1k = m1kw*(mw[0]+mw[1])/mw[0]
            m2k = m2kw*(mw[0]+mw[1])/mw[1]
            mm1c = m1k/(m1k+m2k)
            sh.write(ss,0,"{:10.4f}".format(cv))
            sh.write(ss,1,"{:10.4f}".format(w10[i]))
            sh.write(ss,2,"{:10.4f}".format(m1clc))
            sh.write(ss,3,"{:10.4f}".format(w1))
            sh.write(ss,4,"{:10.4f}".format(m1kw))
            sh.write(ss,5,"{:10.4f}".format(m1k))
            sh.write(ss,6,"{:10.4f}".format(m2clc))
            sh.write(ss,7,"{:10.4f}".format(w2))
            sh.write(ss,8,"{:10.4f}".format(m2kw))
            sh.write(ss,9,"{:10.4f}".format(m2k))
            sh.write(ss,10,"{:10.4f}".format(mm1c))
            ss += 1
        mm1cnv.append(mm1c)
    book.save('conversion.xls')  # { toata partea italic este pentru a scrie rezultatele intr-un fisier excel}
    return mm1cnv

def meth_tm():
    difftm = []
    h1, h2, h3 = 1, 2, 3
    m = len(mm10)
    res_FR1 = meth_fr1()
    r1j, r2j = res_FR1[0], res_FR1[1]
    conf = False
    sj = nlss(r1j, r2j)
    while not conf:
        r11 = r1j + (h1-1)/2*sj
        r21 = r2j + (h1-1)/2*sj
        s1 = nlss(r11,r21)
        print("{:10.4f}".format(r11),"{:10.4f}".format(r21),"{:10.4f}".format(s1))
        r12 = r1j + (h2-1)/2*sj
        r22 = r2j + (h2-1)/2*sj
        s2 = nlss(r12,r22)
        print("{:10.4f}".format(r12),"{:10.4f}".format(r22),"{:10.4f}".format(s2))
        r13 = r1j + (h3-1)/2*sj
        r23 = r2j + (h3-1)/2*sj
        s3 = nlss(r13,r23)
        print("{:10.4f}".format(r13),"{:10.4f}".format(r23),"{:10.4f}".format(s3))
        v = 1/2 + (s1 - s3)/(4*(s1 - 2*s2 + s3))
        cf = False
        while not cf:
            r1v = r1j + v*sj
            r2v = r2j + v*sj
            sv = nlss(r1v, r2v)
            if sv > s1:
                sj = sj/2 
            else:
                r1j = r1v
                r2j = r2v
                cf = True
        j = 0
        del difftm[:]
        for j in range(m):
            difftm.append(mayo_lewis(mm10[j], r1j, r2j) - m1[j])
        stddev = stat.stdev(difftm)
        if stddev < 0.1:
            if r1j < 0:
                r1j = 0.0001
            if r2j < 0:
                r2j = 0.0001
            r1tm = r1j
            r2tm = r2j
            conf = True
    ftm = fischer(mm10,r1tm, r2tm)
    m1ctm = conversion(r1tm,r2tm)
    ftmc = fischer(m1ctm,r1tm,r2tm)
    if (r1tm < 1) and (r2tm < 1):
        aztm = azeotrop(r1tm,r2tm)
    else:
        aztm = 0
    return r1tm, r2tm, ftm, ftmc, aztm

def meth_procop():
    ra1,ra2,fa,m1cc =([] for kpc in range(4))
    ref,exp,cont,shr = 1,2,0.5,0.5
    res_fr1 = meth_fr1()
    res_tm = meth_tm()
    res_kc = meth_kc()
    res_rc = meth_rcop()
    res_std = meth_std()
    ra1 = [res_fr1[0],res_tm[0],res_kc[0],res_rc[0],res_std[0]]
    ra2 = [res_fr1[1],res_tm[1],res_kc[1],res_rc[1],res_std[1]]
    fa = [res_fr1[3],res_tm[3],res_kc[3],res_rc[3],res_std[3]]
    conf = False
    while not conf:
         for i in range(5,0,-1):
           for j in range(0,5-1):
               if fa[j] > fa[j+1]:
                   fi = fa[j]
                   p1i = ra1[j]
                   p2i = ra2[j]
                   fa[j] = fa[j+1]
                   ra1[j] = ra1[j+1]
                   ra2[j] = ra2[j+1]
                   fa[j+1] = fi
                   ra1[j+1] = p1i
                   ra2[j+1] = p2i
         sra1,sra2 = 0,0
         for i in range(4):
             sra1 += ra1[i]
             sra2 += ra2[i]
         r1med = sra1/4;
         r2med = sra2/4
         m1rac = conversion(ra1[1],ra2[1])
         m = len(mm10)
         rr1 = r1med+ref*(r1med-ra1[4])
         rr2 = r2med+ref*(r2med-ra2[4])
         if rr1 < 0:
             rr1 = 0.0001
         if rr2 < 0:
             rr2 = 0.0001
         m1crr = conversion(rr1,rr2)
         frr = fischer(m1crr,rr1,rr2)
         if (frr>=fa[0]) and (frr<fa[3]):
             ra1[4]=rr1
             ra2[4]=rr2
         if frr <= fa[0]:
             re1 = r1med+exp*(rr1-r1med)
             re2 = r2med+exp*(rr2-r2med)
             if re1 < 0:
                 re1 = 0.0001
             if re2 < 0:
                 re2 = 0.0001
             m1ce = conversion(re1,re2)
             fe = fischer(m1ce,re1,re2)
             if fe < frr:
                 ra1[4]=re1
                 ra2[4]=re2
                 fa[4]=fe
             else:
                 ra1[4]=rr1
                 ra2[4]=rr2
                 fa[4]=frr
         if (fa[3]<frr) and (frr<fa[4]):
             roc1 = r1med-cont*(ra1[4]-r1med)
             roc2 = r2med-cont*(ra2[4]-r2med)
             if roc1 < 0:
                 roc1 = 0.0001
             if roc2 < 0:
                 roc2 = 0.0001
             m1coc = conversion(roc1,roc2)
             foc = fischer(m1coc,roc1,roc2)
             if foc <= fa[4]:
                 ra1[4]=roc1
                 ra2[4]=roc2
                 fa[4]=foc
         if frr >= fa[3]:
             r1ic = r1med+cont*(ra1[4]-r1med)
             r2ic = r2med+cont*(ra2[4]-r2med)
             if r1ic < 0:
                 r1ic = 0.0001
             if r2ic < 0:
                 r2ic = 0.0001
             m1cic = conversion(r1ic,r2ic)
             fic = fischer(m1cic,r1ic,r2ic)
             if fic <= fa[4]:
                 ra1[4]=r1ic
                 ra2[4]=r2ic
                 fa[4]=fic
             else:
                 for i in range(1,4):
                     ra1[i]=ra1[0]+shr*(ra1[i]-ra1[0])
                     ra2[i]=ra2[0]+shr*(ra2[i]-ra2[0])
                     if ra1[i] < 0:
                         ra1[i] = 0.0001
                     if ra2[i] < 0:
                         ra2[i] = 0.0001
                     m1cra = conversion(ra1[i],ra2[i])
                     fa[i] = fischer(m1cra,ra1[i],ra2[i])
         for i in range(m):
             m1cc.append(mayo_lewis(m1rac[i],ra1[1],ra2[1])-m1[i])
         err =stat.stdev(m1cc)
         if err < 0.1:
             conf = True
    r1pc = ra1[1]
    r2pc = ra2[1]
    m1cpc = conversion(r1pc,r2pc)
    fpc = fischer(mm10,r1pc,r2pc)
    fpcc = fischer(m1cpc,r1pc,r2pc)
    if (r1pc<1) and (r2pc<1):
        azpc = azeotrop(r1pc,r2pc)
    else:
        azpc = 0
    return r1pc,r2pc,fpc,fpcc,azpc

def Main():
    read_data()
    print()
    print('          r1         r2      F0*1000     Fc*1000   Azeotrope')
    print('--------------------------------------------------------------')
    res_pc = meth_procop()
    print('PC  ',"{:10.5f}".format(res_pc[0]),"{:10.5f}".format(res_pc[1]),"{:10.4f}".format(res_pc[2]),  
                 "{:11.4f}".format(res_pc[3]),"{:10.4f}".format(res_pc[4]))


Main()
