package com.company;

import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.kohsuke.github.*;

import javax.print.DocFlavor;
import javax.xml.ws.http.HTTPException;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        String  password;
        String userName;
        int num=1;
        Map<String, Object[]> data = new HashMap<String, Object[]>();
        SimpleDateFormat simpleDateFormat=new SimpleDateFormat("dd-MM-yyyy");
        data.put("1", new Object[] {"Email Address","Log_in name","User Name","Created_at","Updated_at","profile_link","Commits"});
        GitHub gitHub= null;
        try
        {

            gitHub = GitHub.connectUsingPassword("Username","Password");

            /*List<GHUser> ghUsers=gitHub.searchUsers().q("ethereum").list().asList();*/
            GHRepositorySearchBuilder ghRepositorySearchBuilder=gitHub.searchRepositories();
            ghRepositorySearchBuilder.q("qtum pushed:>2017-01-01");
            ghRepositorySearchBuilder.sort(GHRepositorySearchBuilder.Sort.STARS);
            ghRepositorySearchBuilder.order(GHDirection.DESC);
            GHUser tempUser;
            List<GHRepository> res=null;
            for(;true;) {
                PagedSearchIterable<GHRepository> pagedSearchIterable = ghRepositorySearchBuilder.list();
                try {
                    res = ghRepositorySearchBuilder.list().asList();
                    break;
                } catch (HTTPException e) {
                    continue;

                }
            }
            int counter=1;
            String email;
            int commits;
            List<GHCommit> allcommit=new ArrayList<>();
            for(int i=(100*(num-1));i<res.size();i++)
            {

                tempUser=null;
                List<GHCommit> commits1=null;
                for(;true;) {

                    try {
                        tempUser = res.get(i).getOwner();
                        break;
                    } catch (HTTPException HttpException) {
                        continue;
                    }
                }
                email=tempUser.getEmail();
                PagedIterable<GHCommit> dmtemp;
                for(;(email!=null )&&(email.length()!=0);) {

                    try {

                       dmtemp=res.get(i).queryCommits().since(simpleDateFormat.parse("01-01-2017")).list();
                       commits1=dmtemp.asList();
                       allcommit.addAll(commits1);

                       break;
                    }
                    catch (java.lang.Error e) {
                        break;
                    }catch (Exception e)
                    {

                    }

                }
                System.out.println("Trying list "+i);

                if(email!=null && email.length()!=0 && commits1!=null)
                {
                    counter++;
                    data.put(counter+"", new Object[] {email,tempUser.getLogin(),tempUser.getName(),simpleDateFormat.format(res.get(i).getCreatedAt()),simpleDateFormat.format(res.get(i).getUpdatedAt()),tempUser.getHtmlUrl().toString(),commits1.size()});
                }
                /*if(i!=0 && i%1000==0)
                {
                    fileWriter(data,(i/1000));
                    counter=1;
                }
                if(i==1015)
                {
                    email="vrvrv";
                }*/

            }

            fileWriter(data, "xl/email_address_"+num);
            commitHandler(allcommit,data);
            fileWriter(data,"committer/Committer"+num);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    public  static  void commitHandler(List<GHCommit> commit,Map<String, Object[]> data)
    {
        data.put("1", new Object[] {"Email Address","Log_in name","User Name","profile_link"});
        int counter=1;
        GHUser temp=null;
        for(int i=0;i<commit.size();i++)
        {
            counter++;
            try
            {
                temp=commit.get(i).getAuthor();
                if(temp!=null && temp.getEmail()!=null && temp.getEmail().length()!=0)
                {
                    data.put(counter+"", new Object[] {temp.getEmail(),temp.getLogin(),temp.getName(),temp.getHtmlUrl().toString()});
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    public  static  void fileWriter(Map<String, Object[]>  data,String  fileName)
    {
        HSSFWorkbook workbook = new HSSFWorkbook();
        HSSFSheet sheet = workbook.createSheet("sheet1");



        Set<String> keyset = data.keySet();
        int rownum = 0;
        for (String key : keyset) {
            Row row = sheet.createRow(rownum++);
            Object [] objArr = data.get(key);
            int cellnum = 0;
            for (Object obj : objArr) {
                Cell cell = row.createCell(cellnum++);
                if(obj instanceof Date)
                    cell.setCellValue((Date)obj);
                else if(obj instanceof Boolean)
                    cell.setCellValue((Boolean)obj);
                else if(obj instanceof String)
                    cell.setCellValue((String)obj);
                else if(obj instanceof Double)
                    cell.setCellValue((Double)obj);
                else if(obj instanceof Integer)
                    cell.setCellValue((Integer)obj);
            }
        }

        try {
            FileOutputStream out = new FileOutputStream(new File(fileName+".xls"));
            workbook.write(out);
            out.close();
            System.out.println(fileName+" written successfully..");
            data.clear();


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public  static  List<GHRepository> list(PagedSearchIterable<GHRepository> res)
    {
        ArrayList<GHRepository> temp=new ArrayList<>();
        PagedIterator<GHRepository> iterator=res.iterator();
        for(int i=0;iterator.hasNext();i++)
        {
            temp.add(iterator.next());
        }
        return  temp;
    }
}
