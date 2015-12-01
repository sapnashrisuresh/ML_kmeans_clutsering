#1st	argument:	number	of	clusters	- k
#2nd	argument:	initialization	method - "rand":	random
#											- "first":	select	first	k	points	from	input	file	as	initialized	centroids
#3rd argument:	convergence	threshold	(if	change	between	2	iterations	is	smaller	 than	this	threshold,	converged)
#4th	argument:	maximum	number	of	iterations	(stops	after	max	number	of	trials	even	if	convergence	threshold	not	met)
#5th	argument:	input	file	name


#Compiling instrucitons, run:
# python kmeans.py 3 first 1e-9 50 test

import sys,math,random
from copy import deepcopy

k=sys.argv[1]
initialize=sys.argv[2]
convergence=sys.argv[3]
maxiter=sys.argv[4]
filein=sys.argv[5]

def readdata():
	with open (filein,'r') as file:	
		data=[]
		for line in file.readlines():
			words=line.split(',')
			dimension=len(words)
			d1=[0]*dimension
			i=0
			while i<dimension:
				d1[i]=float(words[i])
				i+=1
			data.append(d1)
		file.close()

	centroid=[]
	newdata=list(data)

	if initialize=="first":
		centroid=deepcopy(data[:int(k)])	
	

	if initialize=="rand":
		random.shuffle(newdata,random.random)
		centroid=deepcopy(newdata[:int(k)])
	
	
	return data,dimension,centroid

def computekmeans(data,dimension,centroid,conflag,b):
	l=0
	b=[]
	for line in data:
		mindistance=1000
		c=0
		b1=[0]*len(centroid)
		for cen in centroid:
			i=0
			distance=0
			while i<dimension:
				distance+=math.pow(float(line[i])-cen[i],2)
				i+=1
			distance=math.sqrt(distance)
			#print(distance)
			if distance<mindistance:
				min=c
				mindistance=distance
			c+=1
			#print(min)
		b1[min]=1
		b.append(b1)
	#print(b)

	totalInCluster=[0]*len(centroid)
	j=0
	difference=0
	while j<len(centroid):
		total=[[0 for x in range(dimension)] for x in range(1)] 
		k=0
		while(k<len(data)):
			d=0
			while(d<dimension):
				if(b[k][j] == 1):
					total[0][d] += data[k][d]
					totalInCluster[j]+=1
				d+=1
			k+=1
		totalInCluster[j]=totalInCluster[j]/dimension

		distance=0
		if(totalInCluster[j] > 0):
			d=0
			while(d<dimension):
				current=centroid[j][d]
				centroid[j][d]=(total[0][d] / totalInCluster[j])
				distance+=math.pow(current-centroid[j][d],2)
				d+=1
			distance=math.sqrt(distance)
		difference+=distance
		j+=1
	if(difference>float(convergence)):
		conflag=True

	return centroid,conflag,b



def main():
	data,dimension,centroid=readdata()
	j=0
	b=[]
	conflag=True
	while j<int(maxiter) and conflag==True:
		centroid,conflag,b=computekmeans(data,dimension,centroid,False,b)
		j+=1

	fileout=filein+".output"
	with open(fileout,'w') as outfile:
		for c in centroid:
			print(c)
			d=0
			while d<dimension:
				if(d!=dimension-1):
					outfile.write(str(c[d])+',')
				else:
					outfile.write(str(c[d])+'\n')
				d+=1

		x=0
		while x<len(b):
			y=0
			while y<len(centroid):
				if b[x][y]==1:
					print(y)
					outfile.write(str(y)+'\n')
				y+=1
			x+=1
		
	

if __name__=='__main__':
	main()