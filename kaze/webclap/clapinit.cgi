######################################################
#
#
#  web拍手CGI基本設定＆主要サブルーチン
#
#
######################################################

#-----------
# 基本設定
#-----------


# 解析にパスワード認証を
# 0…かけない
# 1…かける
$passlock = '0';

# 解析閲覧用パスワード（パスワード認証をかけない場合は不要）
$password = '0000';

# 拍手送信後画面用お礼メッセージ1（タグ使用可）
$message[0]='拍手が送信されました。<br>ありがとうございます。<br><Img src="shed/oebi-01.jpg">';

# 拍手送信後画面用お礼メッセージ2（タグ使用可）
$message[1]='拍手が送信されました。<br>感謝感謝！<br><Img src="shed/oebi-02.jpg">';

# 拍手送信後画面用お礼メッセージ3（タグ使用可）
$message[2]='拍手が送信されました。<br>これからもどうぞよしなに。<br><Img src="shed/oebi-03.jpg">';

# 拍手送信後画面用お礼メッセージ4（タグ使用可）
$message[3]='拍手が送信されました。<br>ありがとうございます。<br><Img src="shed/oebi-04.jpg">';

# 拍手送信後画面用お礼メッセージ5（タグ使用可）
$message[4]='拍手が送信されました。<br>ありがとうございます。励みになります。<br><Img src="shed/oebi-04.jpg">';


# ログファイル
$logfile = './log.dat';

# 一言メッセージ保存ファイル
$mesfile = './mes.dat';

# ファイルロックを
# 0…しない
# 1…する
# かなりの数の拍手が送られてくると思われる場合は1にしてください。
# ファイルロックにはflock関数を使用します。サーバーのＯＳの対応状況をご確認ください
$lock = '0';

# ロックファイル名（ファイルロックをしない場合は不要）
$lockfile = 'lock.dat';

# グラフURL(サーバーによっては絶対パス）
# cgiフォルダに画像が置けないサーバーもあるので注意してください
$graph1 = './graph1.gif';    #横
$graph2 = './graph2.gif';    #縦


#----------
# 設定終了
#----------



#--------------
# HTMLヘッダー
#--------------
sub header{

print "Content-type: text/html\n\n";
print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">',"\n";
print '<html lang="ja"><head>',"\n";
print "<title>$title</title>\n";
print '<link rel="stylesheet" href="../kaze-css.css">',"\n";
print "</head>\n";

}


#----------
# 日付取得
#----------
sub dateload{

$ENV{'TZ'} = "JST-9";
($sec,$min,$tohour,$today,$tomon,$toyear,$wday,$yday,$isdst) = (localtime(time-$day*86400));

$toyear += 1900;
$tomon ++;

$getdate = "$toyear";

if ($tomon <= 9){ $getdate = "$getdate"."0$tomon"; }
         else { $getdate = "$getdate$tomon"; }

if ($today <= 9){ $getdate = "$getdate"."0$today"; }
         else { $getdate = "$getdate$today"; }

}


#------------------
# フォームデコード
#------------------
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	}
	%in=();
	foreach (split(/&/, $buf)) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# S-JISコード変換
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;

		# 改行処理
		if ($key eq "comment") {
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
		} else {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}
		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
        $pass = $in{'pass'};
        $hitokoto = $in{'hitokoto'};
        $kaisuu = $in{'kaisuu'};
}


#---------------------
# ファイルロック開始
#---------------------
sub lockon{

 if ($lock eq '1'){

  open(LOCK,">$lockfile");  #====ロック開始
  flock (LOCK,2);

 }

}

#---------------------
# ファイルロック終了
#---------------------
sub lockoff{

 if ($lock eq '1'){

  unlink( "$lockfile" );
  flock( LOCK, 8 );
  close( LOCK );  #=================ロック終了

 }

}
