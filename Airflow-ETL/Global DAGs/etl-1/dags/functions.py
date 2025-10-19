# functions.py

from libraries import *

def pyspark_init():
  spark = SparkSession.builder.appName("covid19MoleculePrediction").getOrCreate()
  return spark

def categorical_transformation(properties_df, data_df):
  
  """ 
  function to clean dat, removing null, buplicates, and considring only numerical features
  """

  # joining the properties table and dataframe table
  df1=data_df.join(properties_df, on='SMILES', how='inner')
  df1=df1.drop("Compound No.").drop("_c3")

  # pic50 is  present with string, need to cast it into double actual format
  df1=df1.withColumn("target_pIC50", df1["pIC50"].cast("double"))

  #droping null samples if either sample is absent
  df1=df1.dropna(how='any')

  # feqatures of non num type
  alpha_features=[i[0] for i in df1.dtypes if i[1]=="string"]
  df3=df1.drop(*alpha_features)

  # remove those features whose satnddard deviation of features is zero 
  df3=df3.drop(*["Charge","IsotopeAtomCount","DefinedAtomStereoCount","UndefinedBondStereoCount","CovalentUnitCount"])
  return df3

def numerical_transformation(df):
  
  """
  output: scaled_features_vector column which congtins feature vector 

  data will be encoded into vectors as well as minmax scaled fopr better optimization.
  If you had 100 separate numeric columns, Spark could not easily optimize the memory storage for all those zeros across 100 columns
  simultaneously; packing them into a single, compact vector column is much more efficient.
  """
  # if we want to do minmax scaling, then we need to convert those set of features in vectors,
  assembler = VectorAssembler(
      inputCols=["MolecularWeight","MonoisotopicMass","Complexity"],
      outputCol="features_vector"
  )
  df_vector = assembler.transform(df)
  scaler = MinMaxScaler(
    inputCol="features_vector",
    outputCol="scaled_features_vector"
  )

  # final vector matric where initial columns will be numerical features but last feature will be vector matrix, all feature embedded in one column as a vector
  scaler_model = scaler.fit(df_vector).transform(df_vector)
  return scaler_model

def chem_extract():
  """
  As data is structure so we will be use pysaprk dataframe, if data was semistructure of unstuctured like textx, json then we could use RDD(r- distributed dataset) 
  """

  print("extractdata proces from kaggle store initiated")
  path=kagglehub.dataset_download("divyansh22/drug-discovery-data")
  path=kagglehub.dataset_download("divyansh22/drug-discovery-data")
  properties=r"/kaggle/input/drug-discovery-data/DDH Data with Properties.csv"
  data=r"/kaggle/input/drug-discovery-data/DDH Data.csv"

  spark=pyspark_init()
  properties_df = spark.read.csv(
    properties,
    header=True,       # Treat the first row as column names
    inferSchema=True )
  data_df = spark.read.csv(
    data,
    header=True,       # Treat the first row as column names
    inferSchema=True )
  
  print("extract proces completed")
  return properties_df, data_df

def chem_transform():

  print("transform pre/num-proces started")
  # process to extarct features
  properties_df, data_df=chem_extract()

  print("transform pre-proces started")
  # remove null, duplicates abd droping non num features
  df=categorical_transformation(properties_df, data_df)

  print("transform numerical-proces started")
  # converting features into vectors as sparka consider vector for better optimization
  final_dataframe=numerical_transformation(df)
  return final_dataframe

def chem_load():
  print("load process started")
  output_path=r"./final_chemical_comp.csv"
  chem_transform().write.option("header", True).csv(output_path)
  print("load proces completed")
  pass



def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}

