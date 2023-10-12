from gmpy2 import *
import time

N = [
    90058705186558569935261948496132914380077312570281980020033760044382510933070450931241348678652103772768114420567119848142360867111065753301402088676701668212035175754850951897103338079978959810673297215370534716084813732883918187890434411552463739669878295417744080700424913250020348487161014643951785502867,
    92921790800705826977497755832938592891062287903332844896046168726101016067456726822505517352409138948392871113192427210529297191908638888388136391240683157994654207338463678065440899870434887094216772312358731142317774259942199808535233769089985063860828267808621928898445383706310204223006136919334252875849,
    90252653600964453524559669296618135272911289775949194922543520872164147768650421038176330053599968601135821750672685664360786595430028684419411893316074286312793730822963564220564616708573764764386830123818197183233443472506106828919670406785228124876225200632055727680225997407097843708009916059133498338129,
    92270627783020341903769877272635163757611737252302329401876135487358785338853904185572496782685853218459404423868889360808646192858060332110830962463986164014331540336037718684606223893506327126112739408023014900003600028654929488487584130630596342720833061628867179840913592694993869009133576053124769728363,
    90058705186558569935261948496132914380077312570281980020033760044382510933070450931241348678652103772768114420567119848142360867111065753301402088676701668212035175754850951897103338079978959810673297215370534716084813732883918187890434411552463739669878295417744080700424913250020348487161014643951785502867,
    99193711547257063160816850544214924340574358752670644615293764532335872088470223740970673347993652626497557387222167784182876395436088845281840169701654629849214222297784511349059698963212947299142320497759258889425182705042123217476724761095690092179821753840224757786599021225709340258545979566824267620959,
    146839643970016464813197409569004275595828791825722617066607993001682901023784267554815946189374651530288894322286859792246413142980277245909181062525398546369553995023529451396820549308690493928593324007689135648753323161394735120908960458860801743476353228970081369439513197105039143930008573928693059198131,
    155266493936043103849855199987896813716831986416707080645036022909153373110367007140301635144950634879983289720164117794783088845393686109145443728632527874768524615377182297125716276153800765906014206797548230661764274997562670900115383324605843933035314110752560290540848152237316752573471110899212429555149,
    102900163930497791064402577447949741195464555746599233552338455905339363524435647082637326033518083289523250670463907211548409422234391456982344516192210687545692054217151133151915216123275005464229534891629568864361154658107093228352829098251468904800809585061088484485542019575848774643260318502441084765867,
    97767951046154372321400443371234495476461828137251939025051233003462769415459435471728054384852461870179980010660162922547425212869925648424741526671585598167502856111641944825179295197098826911226483155821197251989297102189187139234080795582529077092266799813985026581245196104843272305656744384140745492897,
    93836514358344173762895084384953633159699750987954044414830106276642828025218933012478990865656107605541657809389659063108620208004740646099662700112782252200834393363574089818787717951026690934986964275526538236750596344542450864284576226592039259070002692883820960186403938410354082341916474419847211138467,
    112306066601652819062206435724795595603085908011001671184332227488970057128128821831260649058569739569103298091727188365019228385820143813415009397359257831092635374404034997011441653286642458431865026213129412677064308342580757248577955071384972714557250468686599901682728173096745710849318629959223270431039,
    90267480939368160749458049207367083180407266027531212674879245323647502822038591438536367206422215464489854541063867946215243190345476874546091188408120551902573113507876754578290674792643018845798263156849027209440979746485414654160320058352559498237296080490768064578067282805498131582552189186085941328701,
    94390533992358895550704225180484604016029781604622607833044135524814562613596803297695605669157378162035217814540004231075201420796787547733762265959320018107419058832819010681344133011777479722382525797938558181629835768471461434560813554411133962651212455645589624432040989600687436833459731886703583047283,
    120008876536855131221255979370745233738591934188224528487535120483456214085493237482915446419599357910343450285858995374277365393767669569942204888383426461862651659865189178784473131914234181752055950431093341514138390898892413182538823693941124637301582389014479754627419560568004831093116617428970538503551,
    147733349387696521015664992396355145811249793103958464053225389476050097503928022819269482555955365534137156079172704297584033078453033637103720972881068435459202133846880715879894340131656691631756162323422868846616160423755883726450486845175227682329583615739797782025647376042249605775433971714513081755709,
    90673177193017332602781813187879442725562909473411994052511479411887936365983777106776080722300002656952655125041151156684340743907349108729774157616323863062525593382279143395837261053976652138764279456528493914961780300269591722101449703932139132398288208673556967030162666354552157189525415838326249712949,
    111178307033150739104608647474199786251516913698936331430121060587893564405482896814045419370401816305592149685291034839621072343496556225594365571727260237484885924615887468053644519779081871778996851601207571981072261232384577126377714005550318990486619636734701266032569413421915520143377137845245405768733,
    93394639108667212482180458616036741615058981058942739509025631675767304945732437421192075466824789572910657586684470553691049259504106442090140927782673066834126848556317079995332229262871079799089771973100731889841015960713908117908583988637159206246729697336281050046919985463146705713899703248595045701819,
    94154993593274109828418786834159728190797445711539243887409583756844882924221269576486611543668906670821879426307992404721925623741478677756083992902711765865503466687919799394258306574702184666207180530598057989884729154273423032471322027993848437082723045300784582836897839491321003685598931080456249945287,
    90916739755838083837461026375700330885001446224187511395518230504776419813625940046511904838818660297497622072999229706061698225191645268591198600955240116302461331913178712722096591257619538927050886521512453691902946234986556913039431677697816965623861908091178749411071673467596883926097177996147858865293]

Nd = [
    90252653600964453524559669296618135272911289775949194922543520872164147768650421038176330053599968601135821750672685664360786595430028684419411893316074286312793730822963564220564616708573764764386830123818197183233443472506106828919670406785228124876225200632055727680225997407097843708009916059133498338129,
    146839643970016464813197409569004275595828791825722617066607993001682901023784267554815946189374651530288894322286859792246413142980277245909181062525398546369553995023529451396820549308690493928593324007689135648753323161394735120908960458860801743476353228970081369439513197105039143930008573928693059198131,
    94390533992358895550704225180484604016029781604622607833044135524814562613596803297695605669157378162035217814540004231075201420796787547733762265959320018107419058832819010681344133011777479722382525797938558181629835768471461434560813554411133962651212455645589624432040989600687436833459731886703583047283,
    111178307033150739104608647474199786251516913698936331430121060587893564405482896814045419370401816305592149685291034839621072343496556225594365571727260237484885924615887468053644519779081871778996851601207571981072261232384577126377714005550318990486619636734701266032569413421915520143377137845245405768733,
    94154993593274109828418786834159728190797445711539243887409583756844882924221269576486611543668906670821879426307992404721925623741478677756083992902711765865503466687919799394258306574702184666207180530598057989884729154273423032471322027993848437082723045300784582836897839491321003685598931080456249945287]


def BFFactor(fname, n):  # 细分
    s = time.clock()
    for f16bit in range(1, 65537):
        print('\r', f16bit)
        Xn = bin(f16bit)[2:].zfill(16)
        while len(Xn) < 1000:
            Xn += bin((365 * int(Xn[-16:], 2) - 1) % 2 ** 16)[2:].zfill(16)

        while len(Xn) > 980 and int(Xn, 2):
            # print Xn
            if gcd(int(Xn, 2), n) != 1:
                print('[+]Frame %s Factor found!' % fname)
                print('  [-]Factor1:', int(Xn, 2))
                print('  [-]Factor2:', n / int(Xn, 2))
                print('[!]Timer:', round(time.time() - s), 's')
                return ''

            Xn = Xn[:-1]

    return '[!!!]Factor not found!\n'


def FindFactors(fname, n):  # 小于 512bits
    s = time.time()
    for f16bit in range(1, 65537):
        Xn = bin(f16bit)[2:].zfill(16)
        while len(Xn) < 520:
            # Xn.append(bin((365 * Xn[-1] - 1) % 2**16)[2:])
            Xn += bin((365 * int(Xn[-16:], 2) - 1) % 2 ** 16)[2:].zfill(16)
            # xn = ''.join([bin(i)[2:] for i in Xn])
            if gcd(int(Xn, 2), n) != 1:
                print('[+]Frame %s Factor found!' % fname)
                print('  [-]Factor1:', int(Xn, 2))
                print('  [-]Factor2:', n / int(Xn, 2))
                print('[!]Timer:', round(time.time() - s), 's')
                return ''
    return '[!!!]Factor not found!\n'


s = time.time()
for fname, n in enumerate(N):
    print(FindFactors(fname, n))

print('[!]All Timer:', round(time.time() - s), 's')