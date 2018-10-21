#!/usr/bin/perl --

#########################################
#
# web拍手解析CGI
#
# 作・だんでぃ
#
#########################################

# このCGIのファイル名
$base = "kaiseki.cgi";

#----------外部ファイル読み込み（サーバーによっては絶対パスで指定）
require 'jcode.pl';
require 'clapinit.cgi';

#----------パラメータを取得
$pal = $ENV{'QUERY_STRING'};
($pass,$logday) = split(/&/,$pal);


#----------パラメータの日付が遠すぎないかチェック
if ($logday > 13) {$logday = 0;}
if ($logday eq '') {$logday = 0;}


#----------ＩＤ、パスワード、解析公開認証
&passcheck;

#---------ログの日付をチェック
&logdate;

#----------ログ作成日の日にち取得
$day = $logday;
&dateload;


#---------解析用データ抽出
& makelog;
& makemes;

#---------ログの最高値抽出
$logmax = 0;
for ($i=0 ; $i<=23 ; $i++){

 if ($logmax < $log[$i]){ $logmax = $log[$i]; }

}

#---------過去14日分のトータル抽出
@pasttotal = (0,0,0,0,0,0,0,0,0,0,0,0,0,0);
($pastdate,$pasttotal[0]) = split(/<>/,$logs[$#logs]);
$pastmax = $pasttotal[0];

for ($i=1 ; $i<=13 ; $i++){

 $day=$i;
 &dateload;

 for ($l=0 ; $l<=$#logs ; $l++){

  ($pastdate,$pasttotal) = split(/<>/,$logs[$l]);
  if ($getdate eq $pastdate){ $pasttotal[$i]=$pasttotal; }

 }

 if ($pastmax < $pasttotal[$i]){$pastmax = $pasttotal[$i];}

}


$day = $logday;
&dateload;
#----------------------HTML表示
$title = "web拍手解析";
&header;

print '<body>';
print "<center>\n";

print "$tomon月$today日のweb拍手解析<br><br>\n";


#-----------解析結果表示

print "<table border>\n";

print "<td><center>時間</center></td><td><center>数値</center></td>\n";
print "<td><center>グラフ</center></td><tr>\n";

for ($i=0 ; $i<=23 ; $i++){

 print '<td><font size=2><p align="right">',"$i時</p></font></td>\n";
 print '<td><font size=2><p align="right">',"$log[$i]</p></font></td>\n\n";

  if ($logmax){
   $graph = $log[$i] / $logmax * 400;
   print "<td><IMG src=\"$graph1\" width=\"$graph\" height=\"10\" border=\"0\"></td>";
  }
   else {
    print "<td><IMG src=\"$graph1\" width=\"0\" height=\"10\" border=\"0\"></td>";
   }

 print "<tr>\n";
}

print "<td><center>合計</center></td>";
print "<td><p align=\"right\">$logtotal</p></td>";
print "<td width=\"400\">　</td>";

print "</table><br>\n";

#----------------------メッセージ表示
print "今日送られたメッセージ<br>\n";
print "<table border>\n";

for ($i=0 ; $i<=$#mes ; $i++){

 ($mesday,$meshour,$message) = split(/<>/,$mes[$i]);

 print "<td><p align=\"right\">$meshour時</p></td>\n";
 print "<td>$message</td><tr>\n\n";

 $sousinmessage = "$sousinmessage\n$message";

}

print "</table><br>\n";

#---------------------過去2週間のグラフと別の日へのリンク
print "過去14日間の解析<br>";
print "<table border>\n";

#---------------グラフ
for ($i=0 ; $i<=13 ; $i++){

  if ($pastmax){
   $graph = $pasttotal[$i] / $pastmax * 200;
   print "<td height=200 valign=bottom align=center><IMG src=\"$graph2\" width=\"20\" height=\"$graph\" border=\"0\"></td>\n";
  }
   else {
    print "<td height=200 valign=bottom align=center><IMG src=\"$graph2\" width=\"20\" height=\"0\" border=\"0\"></td>\n";
   }
}

#--------------数値
print "<tr>\n";

for ($i=0 ; $i<=13 ; $i++){

 print "<td><center><font size=2>$pasttotal[$i]</font></center></td>\n"

}

#-------------日にちとリンク
print "<tr>\n";

for ($i=0 ; $i<=13 ; $i++){

 $day=$i;
 &dateload;

 print "<td><center><font size=2><a href=\"$base?$pass&$i\">$tomon月$today日</a></font></center></td>\n";

}

print "</table><br><br>\n";

#------------------著作権表示、公式サイトへのリンク（削除不可）

print "<br>\n";
print '<a href="http://www.webclap.com/" target="_blank"><font size=2>web拍手CGI公式サイト</font></a><br><br><br>',"\n";




print "</center>";
print "</body></html>\n";

exit;





#---------ログ抽出
sub makelog{

#----------ログオープン
&lockon;          #====ロック開始

open(IN,"$logfile");
@logs = <IN>;
close(IN);

&lockoff;       #=================ロック終了


 for ($i=0 ; $i <= $#logs ; $i++){

  ($logdate,$logtotal,$log[0],$log[1],$log[2],$log[3],$log[4],$log[5],$log[6],$log[7],$log[8],$log[9],$log[10],$log[11],$log[12]
     ,$log[13],$log[14],$log[15],$log[16],$log[17],$log[18],$log[19],$log[20],$log[21],$log[22],$log[23])
              = split(/<>/,$logs[$i]);

  if ($logdate eq $getdate) { return; }

 }

 $logdate = $getdate;
 @log = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
 $logtotal = 0;

}

#---------------メッセージ抽出
sub makemes{

 &lockon;  #====ロック開始

 open(IN,"$mesfile");  #===========過去メッセージから読み込み
 @mesdata = <IN>;
 close(IN);

 &lockoff;  #=================ロック終了

 for ($i=0 ; $i <= $#mesdata ; $i++){

  ($mesday,$meshour,$message) = split(/<>/,$mesdata[$i]);

  if ($mesday eq $getdate) { @mes = (@mes,$mesdata[$i]); }

 }

}

#--------------パスワード認証
sub passcheck{

if ($passlock eq 0){ return; }

if ($pass eq $password){ return; }

$title = 'パスワード認証エラー';

&header;

print "<body>\n";
print "<center>\n";
print 'パスワードが違います<br><br>';
print '正しく解析を表示させるには、<br>解析ＣＧＩのＵＲＬの後に "?パスワード" を追加してください。<br>';
print '<br>例：パスワードが"0123"だった場合<br><br>';
print "http://～～～/$base?0123";
print '<br><br>となります。';
print "</center>\n</body></html>";

exit;
}


#-------------------ログの日付チェック
sub logdate{

&lockon;             #ロック開始

open(IN,"$logfile");  #===========ログファイルから読み込み
@logdata = <IN>;
close(IN);

#---------ログの分解
($logdate,$logtotal,$log[0],$log[1],$log[2],$log[3],$log[4],$log[5],$log[6],$log[7],$log[8],$log[9],$log[10],$log[11],$log[12]
     ,$log[13],$log[14],$log[15],$log[16],$log[17],$log[18],$log[19],$log[20],$log[21],$log[22],$log[23])
              = split( /<>/ , $logdata[$#logdata] );

#---------日付取得
$day = 0;
&dateload;

#---------日付チェック
if ($getdate ne $logdate){

#---------日付変更時、ゼロログ追加、過去ログ削除
 @log = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
 $logtotal = 0;
 @logdata = (@logdata,"\n");

 $data = "$getdate<>";

 $data = "$data$logtotal<>";

 for ($i=0 ; $i<=23 ; $i++){
  $data = "$data$log[$i]<>";
 }

 $logdata[$#logata] = "$data\n";


 $day = 14;
 & dateload; 

 $j = $#logdata;
 for ( $i=0 ; $i<=$j ; $i++ ){

  ($logdate,$xxx) = split(/<>/,$logdata[0]);
  if ($logdate < $getdate){shift (@logdata);}

 }

#---------日付変更時、過去ログメッセージ削除
 open(IN,"$mesfile");
 @mesdata = <IN>;
 close(IN);

 $j = $#mesdata;
 for ( $i=0 ; $i<=$j ; $i++ ){

  ($logdate,$xxx) = split(/<>/,$mesdata[0]);
  if ($logdate < $getdate){shift (@mesdata);}

 }

 open(OUT,">$mesfile");
 print OUT @mesdata;
 close(OUT);

}

#---------保存用ログ作成
$day = 0;
& dateload;


$data = "$getdate<>";

$data = "$data$logtotal<>";

for ($i=0 ; $i<=23 ; $i++){
 $data = "$data$log[$i]<>";
}

$logdata[$#logata] = "$data\n";

#---------ログ上書き保存
open(OUT,">$logfile");
print OUT @logdata;
close(OUT);


&lockoff;          #ロック終了

}