import itertools as it
#binn=30
peaks=10
intenscountsratio=0.4
def MakeDic(binn):
	dic={}
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
	s=0
	r=0
	i=0
	f.readline()
	while True:
		line=f.readline()
		if line=="":
			break
		if line[-2]=="S":
			s+=1
		elif line[-2]=="R":
			r+=1
		else:
			i+=1
	f.close()
	posneg={"S":1/(s*binn),"R":-1/(r*binn),"I":0}
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
	f.readline()
	while True:
		line=f.readline()
		if line=="":
			break
		try:
			thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train/"+line.split(",",maxsplit=1)[0]+".csv")
			while True:
				thisline=thisf.readline()
				if thisline=="":
					break
				temp=thisline.split(",")
				molwei=int(float(temp[0].strip())//binn)*binn
				inten=float(temp[1].strip())
				if molwei in dic.keys():
					dic[molwei][0]+=inten*posneg[line[-2]]
					dic[molwei][1]+=1*posneg[line[-2]]
				else:
					dic[molwei]=[inten*posneg[line[-2]],1*posneg[line[-2]]]
			thisf.close()
		except FileNotFoundError:
			i=i
	f.close()
	dic=Standardize(dic)
	return dic
def Standardize(dic):
	intenssum=0
	countssum=0
	for z in dic.values():
		intenssum+=z[0]
		countssum+=z[1]
	intensavg=intenssum/len(dic)
	countsavg=countssum/len(dic)
	intensvar=0
	countsvar=0
	for z in dic.values():
		intensvar+=(z[0]-intensavg)**2
		countsvar+=(z[1]-countsavg)**2
	intensstd=(intensvar/len(dic))**0.5
	countsstd=(countsvar/len(dic))**0.5
	newdic={}
	for z in dic.items():
		if countsstd!=0:
			newdic[z[0]]=z[1][0]/intensstd*intenscountsratio+z[1][1]/countsstd*(1-intenscountsratio)
		else:
			newdic[z[0]]=z[1][0]/intensstd*intenscountsratio+1*(1-intenscountsratio)
	return newdic
def GetPeaks(dic,peaks,version):
	newdic={}
	newdictemp=[]
	for z in dic.items():
		if version==1:
			newdic[abs(z[1])]=z[0]
			newdictemp.append(abs(z[1]))
		if version==2:
			temp=0
			i=-4
			while i<5:
				if z[0]+i in dic.keys():
					temp+=dic[z[0]+i]
				i+=1
			newdic[abs(temp)]=z[0]
			newdictemp.append(abs(temp))
	peakdic={}
	i=0
	while i<peaks:
		found=newdic[max(newdictemp)]
		boolean=True
		for z in peakdic.keys():
			if abs(found-z)<5:
				boolean=False
				break
		if boolean==True:
			f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
			f.readline()
			intensdic=[]
			intensdictemp=[]
			while True:
				line=f.readline()
				if line=="":
					break
				try:
					thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train/"+line.split(",",maxsplit=1)[0]+".csv")
					intenssum=0
					while True:
						thisline=thisf.readline()
						if thisline=="":
							break
						temp=thisline.split(",")
						if version==1:
							molwei=int(float(temp[0].strip())//binn)*binn
							if molwei==found:
								intenssum+=float(temp[1].strip())
							if molwei>found:
								break
						if version==2:
							molwei=int(float(temp[0].strip()))
							if abs(found-molwei)<5:
								intenssum+=float(temp[1].strip())
							if molwei>found+4:
								break
					intensdic.append([intenssum,line[-2]])
					intensdictemp.append(intenssum)
					thisf.close()
				except FileNotFoundError:
					i=i
			f.close()
			intensdictemp.sort()
			result={}
			resulttemp=[]
			j=0
			while j<len(intensdictemp):
				right=0
				wrong=0
				k=0
				while k<len(intensdic):
					if dic[found]>0:
						if intensdic[k][0]<intensdictemp[j]:
							if intensdic[k][1]=="R":
								right+=1
							else:
								wrong+=1
						else:
							if intensdic[k][1]=="S":
								right+=1
							else:
								wrong+=1
					else:
						if intensdic[k][0]<intensdictemp[j]:
							if intensdic[k][1]=="S":
								right+=1
							else:
								wrong+=1
						else:
							if intensdic[k][1]=="R":
								right+=1
							else:
								wrong+=1
					k+=1
				result[right/(right+wrong)]=intensdictemp[j]
				resulttemp.append(right/(right+wrong))
				j+=1
			peakdic[found]=result[max(resulttemp)]
			i+=1
		newdictemp.remove(max(newdictemp))
	return peakdic
def Method1():
	dic=MakeDic(binn)
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
	s=0
	r=0
	i=0
	f.readline()
	pointlist=[]
	while True:
		line=f.readline()
		if line=="":
			break
		if line[-2]=="S":
			s+=1
		elif line[-2]=="R":
			r+=1
		else:
			i+=1
		try:
			thisdic={}
			thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train/"+line.split(",",maxsplit=1)[0]+".csv")
			while True:
				thisline=thisf.readline()
				if thisline=="":
					break
				temp=thisline.split(",")
				molwei=int(float(temp[0].strip())//binn)*binn
				inten=float(temp[1].strip())
				if molwei in thisdic.keys():
					thisdic[molwei][0]+=inten
					thisdic[molwei][1]+=1
				else:
					thisdic[molwei]=[inten,1]
			thisf.close()
			thisdic=Standardize(thisdic)
			point=0
			for z in thisdic.items():
				if z[0] in dic.keys():
					point+=z[1]*dic[z[0]]
			pointlist.append(point)
		except FileNotFoundError:
			i=i
	f.close()
	pointlist.sort()
	judgepoint=pointlist[r]
	"""
	thisdic={}
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Test.csv")
	while True:
		line=f.readline()
		if line=="":
			break
		temp=line.split(",")
		molwei=int(float(temp[0].strip())//binn)*binn
		inten=float(temp[1].strip())
		if molwei in thisdic.keys():
			thisdic[molwei][0]+=inten
			thisdic[molwei][1]+=1
		else:
			thisdic[molwei]=[inten,1]
	thisdic=Standardize(thisdic)
	point=0
	for z in thisdic.items():
		if z[0] in dic.keys():
			point+=z[1]*dic[z[0]]
	print(point)
	f.close()
	"""
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Test.csv")
	f.readline()
	right=0
	wrong=0
	while True:
		line=f.readline()
		if line=="":
			break
		try:
			thisdic={}
			thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Test/"+line.split(",",maxsplit=1)[0]+".csv")
			while True:
				thisline=thisf.readline()
				if thisline=="":
					break
				temp=thisline.split(",")
				molwei=int(float(temp[0].strip())//binn)*binn
				inten=float(temp[1].strip())
				if molwei in thisdic.keys():
					thisdic[molwei][0]+=inten
					thisdic[molwei][1]+=1
				else:
					thisdic[molwei]=[inten,1]
			thisf.close()
			thisdic=Standardize(thisdic)
			point=0
			for z in thisdic.items():
				if z[0] in dic.keys():
					point+=z[1]*dic[z[0]]
			if point>judgepoint:
				if line[-2]=="S":
					right+=1
				else:
					wrong+=1
			else:
				if line[-2]=="R":
					right+=1
				else:
					wrong+=1
		except FileNotFoundError:
			i=i
	f.close()
	print("Judgepoint = "+str(judgepoint))
	print(right/(right+wrong)*100)
def Method2(version):
	if version==1:
		dic=MakeDic(binn)
		peakdic=GetPeaks(dic,peaks,1)
	if version==2:
		dic=MakeDic(1)
		peakdic=GetPeaks(dic,peaks,2)
	result={}
	resulttemp=[]
	for z in peakdic.keys():
		right=0
		wrong=0
		f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
		f.readline()
		while True:
			line=f.readline()
			if line=="":
				break
			try:
				thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train/"+line.split(",",maxsplit=1)[0]+".csv")
				intenssum=0
				while True:
					thisline=thisf.readline()
					if thisline=="":
						break
					temp=thisline.split(",")
					if version==1:
						molwei=int(float(temp[0].strip())//binn)*binn
						if molwei==z:
							intenssum+=float(temp[1].strip())
						if molwei>z:
							break
					if version==2:
						molwei=int(float(temp[0].strip()))
						if abs(z-molwei)<5:
							intenssum+=float(temp[1].strip())
						if molwei>z+4:
							break
				if intenssum<peakdic[z]:
					if dic[z]>0:
						if line[-2]=="R":
							right+=1
						else:
							wrong+=1
					else:
						if line[-2]=="S":
							right+=1
						else:
							wrong+=1
				else:
					if dic[z]>0:
						if line[-2]=="S":
							right+=1
						else:
							wrong+=1
					else:
						if line[-2]=="R":
							right+=1
						else:
							wrong+=1
				thisf.close()
			except FileNotFoundError:
				i=i
		f.close()
		result[right/(right+wrong)]=z
		resulttemp.append(right/(right+wrong))
	for z in it.combinations(peakdic.keys(),2):
		zintens=[0,0]
		rights=0
		rightr=0
		wrongs=0
		wrongr=0
		f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train.csv")
		f.readline()
		while True:
			line=f.readline()
			if line=="":
				break
			try:
				thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Train/"+line.split(",",maxsplit=1)[0]+".csv")
				while True:
					thisline=thisf.readline()
					if thisline=="":
						break
					temp=thisline.split(",")
					if version==1:
						molwei=int(float(temp[0].strip())//binn)*binn
						if molwei==z[0]:
							zintens[0]+=float(temp[1].strip())
						if molwei==z[1]:
							zintens[1]+=float(temp[1].strip())
						if molwei>z[0] and molwei>z[1]:
							break
					if version==2:
						molwei=int(float(temp[0].strip()))
						if abs(z[0]-molwei)<5:
							zintens[0]+=float(temp[1].strip())
						if abs(z[1]-molwei)<5:
							zintens[1]+=float(temp[1].strip())
						if molwei>z[0]+4 and molwei>z[1]+4:
							break
				if dic[z[0]]>0 and dic[z[1]]>0:
					if zintens[0]<peakdic[z[0]] and zintens[1]<peakdic[z[1]]:
						if line[-2]=="R":
							rights+=1
						else:
							wrongs+=1
					else:
						if line[-2]=="S":
							rights+=1
						else:
							wrongs+=1
					if zintens[0]>peakdic[z[0]] and zintens[1]>peakdic[z[1]]:
						if line[-2]=="S":
							rightr+=1
						else:
							wrongr+=1
					else:
						if line[-2]=="R":
							rightr+=1
						else:
							wrongr+=1
				elif dic[z[0]]>0 and dic[z[1]]<0:
					if zintens[0]<peakdic[z[0]] and zintens[1]>peakdic[z[1]]:
						if line[-2]=="R":
							rights+=1
						else:
							wrongs+=1
					else:
						if line[-2]=="S":
							rights+=1
						else:
							wrongs+=1
					if zintens[0]>peakdic[z[0]] and zintens[1]<peakdic[z[1]]:
						if line[-2]=="S":
							rightr+=1
						else:
							wrongr+=1
					else:
						if line[-2]=="R":
							rightr+=1
						else:
							wrongr+=1
				elif dic[z[0]]<0 and dic[z[1]]>0:
					if zintens[0]>peakdic[z[0]] and zintens[1]<peakdic[z[1]]:
						if line[-2]=="R":
							rights+=1
						else:
							wrongs+=1
					else:
						if line[-2]=="S":
							rights+=1
						else:
							wrongs+=1
					if zintens[0]<peakdic[z[0]] and zintens[1]>peakdic[z[1]]:
						if line[-2]=="S":
							rightr+=1
						else:
							wrongr+=1
					else:
						if line[-2]=="R":
							rightr+=1
						else:
							wrongr+=1
				else:
					if zintens[0]>peakdic[z[0]] and zintens[1]>peakdic[z[1]]:
						if line[-2]=="R":
							rights+=1
						else:
							wrongs+=1
					else:
						if line[-2]=="S":
							rights+=1
						else:
							wrongs+=1
					if zintens[0]<peakdic[z[0]] and zintens[1]<peakdic[z[1]]:
						if line[-2]=="S":
							rightr+=1
						else:
							wrongr+=1
					else:
						if line[-2]=="R":
							rightr+=1
						else:
							wrongr+=1
				thisf.close()
			except FileNotFoundError:
				i=i
		f.close()
		result[rights/(rights+wrongs)]=(z,"S")
		resulttemp.append(rights/(rights+wrongs))
		result[rightr/(rightr+wrongr)]=(z,"R")
		resulttemp.append(rightr/(rightr+wrongr))
	judgepeaks=result[max(resulttemp)]
	if str(type(judgepeaks))=="<class 'int'>":
		judgepeaksintens=0
	else:
		judgepeaksintens=[0,0]
	f=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Test.csv")
	f.readline()
	right=0
	wrong=0
	while True:
		line=f.readline()
		if line=="":
			break
		try:
			thisdic={}
			thisf=open(r"/Users/EthanAlex/Desktop/Python/新自行練習/Big Data Test/"+line.split(",",maxsplit=1)[0]+".csv")
			if str(type(judgepeaks))=="<class 'int'>":
				judgepeaksintens=0
			else:
				judgepeaksintens=[0,0]
			while True:
				thisline=thisf.readline()
				if thisline=="":
					break
				temp=thisline.split(",")
				if version==1:
					molwei=int(float(temp[0].strip())//binn)*binn
					if str(type(judgepeaks))=="<class 'int'>":
						if molwei==judgepeaks:
							judgepeaksintens+=float(temp[1].strip())
						if molwei>judgepeaks:
							break
					else:
						if molwei==judgepeaks[0][0]:
							judgepeaksintens[0]+=float(temp[1].strip())
						if molwei==judgepeaks[0][1]:
							judgepeaksintens[1]+=float(temp[1].strip())
						if molwei>judgepeaks[0][0] and molwei>judgepeaks[0][1]:
							break
				if version==2:
					molwei=int(float(temp[0].strip()))
					if str(type(judgepeaks))=="<class 'int'>":
						if abs(judgepeaks-molwei)<5:
							judgepeaksintens+=float(temp[1].strip())
						if molwei>judgepeaks+4:
							break
					else:
						if abs(judgepeaks[0][0]-molwei)<5:
							judgepeaksintens[0]+=float(temp[1].strip())
						if abs(judgepeaks[0][1]-molwei)<5:
							judgepeaksintens[1]+=float(temp[1].strip())
						if molwei>judgepeaks[0][0]+4 and molwei>judgepeaks[0][1]+4:
							break
			thisf.close()
			if str(type(judgepeaks))=="<class 'int'>":
				if dic[judgepeaks]>0:
					if judgepeaksintens<peakdic[judgepeaks]:
						if line[-2]=="R":
							right+=1
						else:
							wrong+=1
					else:
						if line[-2]=="S":
							right+=1
						else:
							wrong+=1
				else:
					if judgepeaksintens<peakdic[judgepeaks]:
						if line[-2]=="S":
							right+=1
						else:
							wrong+=1
					else:
						if line[-2]=="R":
							right+=1
						else:
							wrong+=1
			else:
				if dic[judgepeaks[0][0]]>0 and dic[judgepeaks[0][1]]>0:
					if judgepeaks[1]=="S":
						if judgepeaksintens[0]<peakdic[judgepeaks[0][0]] and judgepeaksintens[1]<peakdic[judgepeaks[0][1]]:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
					else:
						if judgepeaksintens[0]>peakdic[judgepeaks[0][0]] and judgepeaksintens[1]>peakdic[judgepeaks[0][1]]:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
				elif dic[judgepeaks[0][0]]>0 and dic[judgepeaks[0][1]]<0:
					if judgepeaks[1]=="S":
						if judgepeaksintens[0]<peakdic[judgepeaks[0][0]] and judgepeaksintens[1]>peakdic[judgepeaks[0][1]]:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
					else:
						if judgepeaksintens[0]>peakdic[judgepeaks[0][0]] and judgepeaksintens[1]<peakdic[judgepeaks[0][1]]:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
				elif dic[judgepeaks[0][0]]<0 and dic[judgepeaks[0][1]]>0:
					if judgepeaks[1]=="S":
						if judgepeaksintens[0]>peakdic[judgepeaks[0][0]] and judgepeaksintens[1]<peakdic[judgepeaks[0][1]]:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
					else:
						if judgepeaksintens[0]<peakdic[judgepeaks[0][0]] and judgepeaksintens[1]>peakdic[judgepeaks[0][1]]:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
				else:
					if judgepeaks[1]=="S":
						if judgepeaksintens[0]>peakdic[judgepeaks[0][0]] and judgepeaksintens[1]>peakdic[judgepeaks[0][1]]:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
					else:
						if judgepeaksintens[0]<peakdic[judgepeaks[0][0]] and judgepeaksintens[1]<peakdic[judgepeaks[0][1]]:
							if line[-2]=="S":
								right+=1
							else:
								wrong+=1
						else:
							if line[-2]=="R":
								right+=1
							else:
								wrong+=1
		except FileNotFoundError:
			i=i
	f.close()
	print("Judgepeaks =",judgepeaks)
	print(right/(right+wrong)*100)
#Method1()
#Method2(1)
Method2(2)