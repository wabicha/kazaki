#!/usr/bin/perl --

#########################################
#
# web拍手送信CGI
#
# 作・だんでぃ
#
#########################################

# このCGIのファイル名
$base = "./clap.cgi";

#----------外部ファイル読み込み（サーバーによっては絶対パスで指定）
require './jcode.pl';
require './clapinit.cgi';

#---------フォームデコード
&decode;


#########################################

#---------ログの読み込み、加算、保存

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

#---------ログ加算
$log[$tohour] ++;
$logtotal ++;

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

#---------------------------------------一言メッセージ処理
if ($hitokoto ne ''){

$mesdata = "$getdate<>$tohour<>$hitokoto<>\n";

open(OUT,">>$mesfile");
print OUT $mesdata;
close(OUT);

}


&lockoff;          #ロック終了


#-----------------------------------ＨＴＭＬ表示
$title = "web拍手送信完了";

&header;

print "<body class=clap>\n";

#------メッセージ
$i = int(rand(4));

print "<center>\n";

print "$message[$i]<br><br><br>\n";

#====================さらに送るフォーム＆メッセージ

if ($kaisuu < 9){

 $kaisuu ++;

 print "<FORM action=$base method=POST>\n";
 print '<INPUT class="clap" type="submit" value="もっと送る"><br><br>',"\n";
 print "<input type=hidden name=kaisuu value=$kaisuu>\n";
 print '何か一言あれば、どうぞ。<br>',"\n";
 print '<input class=nor type=text name=hitokoto size=50 maxlength=200><br>',"\n";
 print '</FORM>',"\n";

}else{

 print '<font size=2>いたずら防止のため、10回以上連続で拍手を送れないようになっています。</font>';

}

print "<br>\n";


#---------------------著作権表示、web拍手公式サイトへのリンク（削除不可）
print '<a href="http://www.webclap.com/" target="_blank">*web拍手CGI公式サイト*</font></a><br>',"\n";



print "</center>\n";
print "</body></html>\n";

exit;
