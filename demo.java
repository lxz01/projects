import org.apache.spark.sql.hive.HiveContext
val hiveContext=new org.apache.spark.sql.hive.HiveContext(sc)
import org.apache.spark.sql.SaveMode
val pageType=hiveContext.sql("select substring(page_type,1,3) as page_type,count(*) as count_num,round((count(*)/837450.0)*100,4) as weights from law group by substring(page_type,1,3)")
pageType.orderBy(-pageType("count_num")).show()
pageType.repartition(1).save("/user/root/sparkSql/pageType.json","json",SaveMode.Overwrite)