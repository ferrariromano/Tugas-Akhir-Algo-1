import json,time,os,datetime

path1= 'pinjaman.json'
path2= 'koleksi.json'

def reset():
    os.system('cls')

def muat_pinjaman():
    try : 
        with open(path1, 'r' ) as file:
            data = json.load(file)
            return data
    except :
        with open(path1, 'w') as file:
            data_kosong = []
            json.dump(data_kosong,file,indent=2)
            return data_kosong

def muat_koleksi():
    with open(path2,'r') as file:
        data = json.load(file)
        return data

def tulis_pinjaman(data_baru):
    with open(path1, 'w') as file:
        json.dump(data_baru,file,indent=2)

def tulis_koleksi(data_baru):
    with open(path2, 'w') as file:
        json.dump(data_baru, file, indent=2)

def menu_kelompok_buku():
    reset()
    while True:
        print('1. Sains')
        print('2. Ekonomi')
        print('3. Politik')
        print('4. Novel')
        print('5. Komik')
        print ('Masukan 0 jika ingin kembali ke menu.')
        try:
            no_kelompok = int(input('Masukan Nomor Kelompok buku : '))
        except Exception:
            print('Masukan Tidak Valid!')
            time.sleep(2)
            reset()
            continue
        if 0 < no_kelompok  < 6:
            break
        elif no_kelompok == 0:
            menu_awal()
        print('Masukan Tidak Valid!')
        time.sleep(2)
        reset()
    return no_kelompok

def Str_KeDate(str1):
    tanggal = datetime.datetime.strptime(str1,'%Y %m %d' )
    return tanggal

def tabel_pinjaman():
    pinjaman = muat_pinjaman()
    #header
    print('+'+'='*5+'+'+'='*5+'+'+'='*15+'+'+'='*40+'+'+'='*20+'+'+'='*15+'+')
    print('|{:^5}|{:^5}|{:^15}|{:^40}|{:^20}|{:^15}|'.format('No','Kode','Nama','Judul','Status','Denda'))
    print('+'+'='*5+'+'+'='*5+'+'+'='*15+'+'+'='*40+'+'+'='*20+'+'+'='*15+'+')

    #body table
    if pinjaman == []:
        print (f'|{"Belum ada buku yang di pinjam!":^62}|')
        return 0
    tanggal = [Str_KeDate(value) for peminjam  in pinjaman for key,value in peminjam.items() if key == 'tanggal'] #iterasi list 'pinjaman --> panggil string tanggal di tiap iterasi --> ubah tanggal string ke date

    #perhitungan status dan denda menggunakan tanggal
    status = []
    denda = []
    sekarang = datetime.datetime.today()
    for x in tanggal:
        tenggat = x + datetime.timedelta(8)
        selisih = (tenggat - sekarang).days
        if selisih < 0 : #denda = hari x Rp.500
            selisih = abs(selisih)   
            hitung_denda = selisih*500
            status.append('Terlambat '+str(selisih)+' hari')
            denda.append('Rp.'+str(hitung_denda)) 
        else:
            status.append('Sisa '+str(selisih)+' hari')
            denda.append('Rp.0')
   
    nomor = 1
    for i,x,y in zip(pinjaman,status,denda):
        if i != []:
            print('|{:^5}|{:^5}|{:^15}|{:^40}|{:^20}|{:^15}|'.format(nomor,i['kode'],i['nama'], i['judul'],x,y))
            nomor += 1
    print('+'+'='*5+'+'+'='*5+'+'+'='*15+'+'+'='*40+'+'+'='*20+'+'+'='*15+'+')

def tabel_buku(no_kelompok):
    koleksi = muat_koleksi()
    reset()
    # Heading
    print('+'+'='*5+'+'+'='*6+'='*45+'+')
    print(f"|{'No':^5}|{'Judul':^51}|")
    print('+'+'='*5+'+'+'='*6+'='*45+'+')
    # body table
    for index, buku in enumerate(koleksi[no_kelompok-1],start=1):
        print('|{0:^5}|{1:^51}|'.format(index,buku['judul']))
    print('+'+'='*5+'+'+'='*6+'='*45+'+')
    return no_kelompok

def tambah_peminjam():
    pinjam = muat_pinjaman()
    koleksi = muat_koleksi()

    #memu 
    nomor_menu = menu_kelompok_buku()
    reset()
    no_kelompok = tabel_buku(nomor_menu)
    while True:
        print('Ketik 0 jika ingin kembali ke menu.')
        index_judul = int(input('Pilih nomor buku yang akan dipinjam : '))
        if 0 < index_judul  <= len(koleksi[no_kelompok-1]):
            break
        elif index_judul == 0:
            menu_awal()
        else:
            print('Masukan Tidak Valid!')

    # input data
    nama = input('Nama peminjam : ')
    sekarang = datetime.date.today()
    judul =koleksi[no_kelompok-1][index_judul-1]['judul']
    kode=koleksi[no_kelompok-1][index_judul-1]['kode']
    
    pinjaman_baru = {
        'nama':nama,
        'judul':judul,
        'tanggal':sekarang.strftime('%Y %m %d'),
        'kode':kode}

    pinjam.append(pinjaman_baru)
    tulis_pinjaman(pinjam)
    del koleksi[no_kelompok-1][index_judul-1]
    tulis_koleksi(koleksi)
    
    print('Buku Berhasil di Pinjam!')
    time.sleep(2)
    reset()
    menu_awal()

def hapus_pinjaman():#pengembalian buku
    reset()
    pinjaman = muat_pinjaman()
    koleksi = muat_koleksi()
    if tabel_pinjaman() == 0 :
        print ('Di alihkan ke menu awal!')
        time.sleep(3)
        menu_awal()
    print('Ketik 0 jika ingin kembali ke menu.')
    nomor = int(input('Pilih Nomor yang akan di hapus : '))
    if nomor == 0 : menu_awal()


    buku_yg_dikembalikan = {key:value for key,value in  pinjaman[nomor-1].items() if key!='nama'} #filter key tanpa 'nama'
    kode = pinjaman[nomor-1]['kode']
    if kode == "A":
        koleksi[0].append(buku_yg_dikembalikan)
        tulis_koleksi(koleksi)
    elif kode =="B":
        koleksi[1].append(buku_yg_dikembalikan)
        tulis_koleksi(koleksi)
    elif kode == 'C':
        koleksi[2].append(buku_yg_dikembalikan)
        tulis_koleksi(koleksi)
    elif kode == 'D':
        koleksi[3].append(buku_yg_dikembalikan)
        tulis_koleksi(koleksi)
    else :
        koleksi[4].append(buku_yg_dikembalikan)
        tulis_koleksi(koleksi)

    pinjaman.pop(nomor-1)
    tulis_pinjaman(pinjaman)
    
    print ("Buku Berhasil dikembalikan!")
    time.sleep(2)
    reset()
    menu_awal()

def tambah_koleksi_buku():
    reset()
    koleksi = muat_koleksi()     
    pilih=menu_kelompok_buku()
    
    kelompok = ['Sains','Ekonomi','Politik','Novel','Komik']
    kode = 'ABCDE'
    buku_baru= input('Masukan judul buku baru     : ')
    
    data_buku_baru = {
        'judul':buku_baru,
        'kode':kode[pilih-1],
        'tanggal': None
    }

    koleksi[pilih-1].append(data_buku_baru)
    tulis_koleksi(koleksi)

    reset()
    print(f'\n{"BUKU BERHASIL DITAMBAHKAN":^75}')
    print ('+'+'='*73+'+')
    print("|Judul Baru : {:^60}|".format(buku_baru))
    print("|Kelompok   : {:^60}|".format(kelompok[pilih-1]))
    print("|Kode       : {:^60}|".format(kode[pilih-1]))
    print ('+'+'='*73+'+')
    time.sleep(3)
    menu_awal()

def hapus_koleksi():
    koleksi = muat_koleksi()
    pilih = menu_kelompok_buku()
    no_kelompok= tabel_buku(pilih)

    while True:
        print('Ketik 0 jika ingin kembali ke menu.')
        index_judul = int(input('Pilih nomor buku yang akan dihapus : '))
        if 0 < index_judul  <= len(koleksi[no_kelompok-1]):
            break
        elif index_judul == 0:
            menu_awal()
        else:
            print('Masukan Tidak Valid!')

    koleksi[no_kelompok-1].pop(index_judul-1)
    tulis_koleksi(koleksi)

    print('\n Buku Berhasil dihapus dari koleksi!')
    time.sleep(2)
    reset()
    menu_awal()

def lihat_koleksi():
    reset()
    nomor = menu_kelompok_buku()    
    tabel_buku(nomor)

    while True:
        print("Ketik 1 untuk kembali memilih kelompok buku kembali")
        print('Ketik 2 untuk kembali ke menu awal ')
        pilihan = input("Masukan Pilihan : ")

        if pilihan == '1':
            lihat_koleksi()
        elif pilihan == '2':
            menu_awal()
        else :
            print('Pilihan tidak valid!')
            time.sleep(2)
            reset()
            tabel_buku(nomor)
            
def menu_awal():
    reset()
    print('-'*38+'SISTEM PERPUSATAKAAN SEDERHANA'+'-'*39)
    tabel_pinjaman()
    print('1. Lihat Koleksi Buku')
    print('2. Tambah Peminjam Buku')
    print('3. Pengembalian Buku')
    print('4. Tambahkan Koleksi Baru Buku')
    print('5. Hapus Koleksi Buku')
    print('6. Suting Nama peminjam')
    print('7. Keluar')
    
    pilih_menu=input('Masukan nomor menu : ')

    if pilih_menu == '1':
        lihat_koleksi()
    elif pilih_menu == '2':
        tambah_peminjam()
    elif pilih_menu == '3':
        hapus_pinjaman()
    elif pilih_menu =='4':
        tambah_koleksi_buku()
    elif pilih_menu == '5':
        hapus_koleksi()
    elif pilih_menu == '6':
        suting_nama()
    elif pilih_menu =='7':
        reset()
        print(f'\n\n{"Dapat Dimengerti, Semoga Harimu Menyenangkan!":^70}\n\n')
        quit()
    else:
        print('Masukan tidak valid!')
        time.sleep(2)
        menu_awal()

def suting_nama():
    reset()
    peminjam = muat_pinjaman ()
    print('-'*45+'Penghapusan Nama'+'-'*45)
    tabel_pinjaman()
    print('Ketik 0 untuk kembali ke menu awal.')
    try:
        index = (int(input("Masuka nomor yang akan diubah : "))-1)
        if index == -1:
            menu_awal()
        elif 0 > index or index >= len(peminjam):
            print("Masukan tidak valid!")
            time.sleep(2)
            suting_nama()

    except Exception:
        print("Masukan tidak valid!")
        time.sleep(2)
        suting_nama()
    
    nama = input("Masukan nama baru : ")
    nama_baru = {
        "nama":nama,
        'judul': peminjam [index]['judul'],
        'tanggal':peminjam[index]['tanggal'],
        'kode':peminjam[index]['kode']
    }
    peminjam [index]=nama_baru
    tulis_pinjaman(peminjam)

    print("Nama Berhasil disuting!")
    menu_awal()
    
menu_awal()