"""
#########################################################################################################
            Converting CSV to libsvm Data Format
#########################################################################################################
"""

import sys
import csv
import operator
from collections import defaultdict
label_index = 0

def construct_line( label, line ): 
  new_line = [] 
  if float( label ) == 0.0: 
    label = "0" 
  new_line.append( label )

  for i, item in enumerate( line ): 
    if len(item.strip())==0 or float( item ) == 0.0: 
      continue # sparse!!! 
    new_item = "%s:%s" % ( i + 1, item ) 
    new_line.append( new_item ) 
  new_line = " ".join( new_line ) 
  new_line += "\n" 
  return new_line

def csv2libsvm(input_file,output_file):
  i = open( input_file, "r")
  o = open( output_file, 'w' )
  reader = csv.reader( i )  
  for line in reader:
    if label_index == -1:
      label = '1'
    else:
      label = line.pop( label_index )
    new_line = construct_line( label, line )
    o.write( new_line )

csv2libsvm('/home/Sathvik/Desktop/OpenSet/W-SVM/train.csv','/home/Sathvik/Desktop/OpenSet/W-SVM/train')
csv2libsvm('/home/Sathvik/Desktop/OpenSet/W-SVM/test.csv','/home/Sathvik/Desktop/OpenSet/W-SVM/test')
