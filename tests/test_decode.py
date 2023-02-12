import pytest

from bolt11.decode import decode

default_expiry = 1000

class TestDecode:
    @pytest.mark.parametrize(
        "name, payment_request, amount, currency, date, payment_hash, features, payee, payment_secret, "
        "signature, description, description_hash, expiry",
        [
            (
                # Please make a donation of any amount using payment_hash 0001020304050607080900010203040506070809000102030405060708090102
                # to me @03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad
                "invoice_1",
                "lnbc1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rq"
                "wzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2ursdae8g6twvus8g6rfwvs8qun0dfjkxaq9qrsgq357wnc5r2ueh7ck6q93dj32dlqnls087fx"
                "dwk8qakdyafkq3yap9us6v52vjjsrvywa6rt52cm9r9zqt8r2t7mlcwspyetp5h2tztugp9lfyql",
                None,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "8d3ce9e28357337f62da0162d9454df827f83cfe499aeb1c1db349d4d81127425e434ca29929406c23bba1ae8ac6ca32880b38d4bf6ff874024cac34ba9625f1",
                "Please consider supporting this project",
                None,
                default_expiry,
            ),
            (
                # Please send $3 for a cup of coffee to the same peer, within one minute
                "invoice_2",
                "lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rq"
                "wzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpu9qrsgquk0rl77nj30yxdy8j9vdx85fkpmdla2087ne0xh8nhedh"
                "8w27kyke0lp53ut353s06fv3qfegext0eh0ymjpf39tuven09sam30g4vgpfna3rh",
                250_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "e59e3ffbd3945e4334879158d31e89b076dff54f3fa7979ae79df2db9dcaf5896cbfe1a478b8d2307e92c88139464cb7e6ef26e414c4abe33337961ddc5e8ab1",
                "1 cup coffee",
                None,
                60,
            ),
            (
                # Please send 0.0025 BTC for a cup of nonsense (ナンセンス 1杯) to the same peer, within one minute
                "invoice_3",
                "lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rq"
                "wzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpu9qrsgqhtjpauu9ur7fw2thcl4y9vfvh4m9wlfyz"
                "2gem29g5ghe2aak2pm3ps8fdhtceqsaagty2vph7utlgj48u0ged6a337aewvraedendscp573dxr",
                250_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "bae41ef385e0fc972977c7ea42b12cbd76577d2412919da8a8a22f9577b6507710c0e96dd78c821dea16453037f717f44aa7e3d196ebb18fbb97307dcb7336c3",
                "ナンセンス 1杯",
                None,
                60,
            ),
            (
                # Now send $24 for an entire list of things (hashed)
                "invoice_4",
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwz"
                "qfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqs9qrsgq7ea976txfraylvgzuxs8"
                "kgcw23ezlrszfnh8r6qtfpr6cxga50aj6txm9rxrydzd06dfeawfk6swupvz4erwnyutnjq7x39ymw6j38gp7ynn44",
                2_000_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "f67a5f696648fa4fb102e1a07b230e54722f8e024cee71e80b4847ac191da3fb2d2cdb28cc32344d7e9a9cf5c9b6a0ee0582ae46e9938b9c81e344a4dbb5289d",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # The same, on testnet, with a fallback address mk2QpYatsKicvFVuTAQLBryyccRXMUaGHP
                "invoice_5",
                "lntb20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhdzgynm4zwqd5d7"
                "xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfpp3x9et2e20v6pu37c5d9va"
                "x37wxq72un989qrsgqdj545axuxtnfemtpwkc45hx9d2ft7x04mt8q7y6t0k2dge9e7h8kpy9p34ytyslj3yu569aalz2xdk8xkd7ltxqld94u8h2esmsmacgpghe9k8",
                2_000_000_000,
                "tb",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "6ca95a74dc32e69ced6175b15a5cc56a92bf19f5dace0f134b7d94d464b9f5cf6090a18d48b243f289394d17bdf89466d8e6b37df5981f696bc3dd5986e1bee1",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # On mainnet, with fallback address 1RustyRX2oai4EYYDpQGWvEL62BBGqN9T with extra routing
                # info to go via nodes 029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255
                # then 039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255
                "invoice_6",
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq"
                "5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqsfpp3qjmp7lwpagxun9pygexvgpjdc4jdj85fr9yq20q82gph"
                "p2nflc7jtzrcazrra7wwgzxqc8u7754cdlpfrmccae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqvpeuqafqxu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhp"
                "hu9y00rrhy4grqszsvpcgpy9qqqqqqgqqqqq7qqzq9qrsgqdfjcdk6w3ak5pca9hwfwfh63zrrz06wwfya0ydlzpgzxkn5xagsqz7x9j4jwe7yj7va"
                "f2k9lqsdk45kts2fd0fkr28am0u4w95tt2nsq76cqw0",
                2_000_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "6a6586db4e8f6d40e3a5bb92e4df5110c627e9ce493af237e20a046b4e86ea200178c59564ecf892f33a9558bf041b6ad2cb8292d7a6c351fbb7f2ae2d16b54e",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # On mainnet, with fallback (P2SH) address 3EktnHQD7RiAE6uzMj2ZifT9YgRrkSgzQX
                "invoice_7",
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy04"
                "3l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfppj3a24vwu6r8ejrss3axul8rxldph2q7z99qrsgqz6qsgww34xla"
                "tfj6e3sngrwfy3ytkt29d2qttr8qz2mnedfqysuqypgqex4haa2h8fx3wnypranf3pdwyluftwe680jjcfp438u82xqphf75ym",
                2_000_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "16810439d1a9bfd5a65acc61340dc92448bb2d456a80b58ce012b73cb5202438020500c9ab7ef5573a4d174c811f669885ae27f895bb3a3be52c243589f87518",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # On mainnet, with fallback (P2WPKH) address bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4
                "invoice_8",
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98kl"
                "ysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfppqw508d6qejxtdg4y5r3zarvary0c5xw7k9qrsgqt2"
                "9a0wturnys2hhxpner2e3plp6jyj8qx7548zr2z7ptgjjc7hljm98xhjym0dg52sdrvqamxdezkmqg4gdrvwwnf0kv2jdfnl4xatsqmrnsse",
                2_000_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "5a8bd7b97c1cc9055ee60cf2356621f8752248e037a953886a1782b44a58f5ff2d94e6bc89b7b514541a3603bb33722b6c08aa1a3639d34becc549a99fea6eae",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # On mainnet, with fallback (P2WSH) address bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3
                "invoice_9",
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw"
                "5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfp4qrp33g0q5c5txsp9arysrx4k6zd"
                "kfs4nce4xj0gdcccefvpysxf3q9qrsgq9vlvyj8cqvq6ggvpwd53jncp9nwc47xlrsnenq2zp70fq83qlgesn4u3uyf4tesfkkwwfg3qs"
                "54qe426hp3tz7z6sweqdjg05axsrjqp9yrrwc",
                2_000_000_000,
                "bc",
                1496314658,
                "0001020304050607080900010203040506070809000102030405060708090102",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "2b3ec248f80301a421817369194f012cdd8af8df1c279981420f9e901e20fa3309d791e11355e609b59ce4a220852a0cd55ab862b1785a83b206c90fa74d01c8",
                None,
                "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
                default_expiry,
            ),
            (
                # Please send 0.00967878534 BTC for a list of items within one week, amount in pico-BTC
                "invoice_10",
                "lnbc9678785340p1pwmna7lpp5gc3xfm08u9qy06djf8dfflhugl6p7lgza6dsjxq454gxhj9t7a0sd8dgfkx7cmtwd68yetpd5s9xar0w"
                "fjn5gpc8qhrsdfq24f5ggrxdaezqsnvda3kkum5wfjkzmfqf3jkgem9wgsyuctwdus9xgrcyqcjcgpzgfskx6eqf9hzqnteypzxz7fzypf"
                "hg6trddjhygrcyqezcgpzfysywmm5ypxxjemgw3hxjmn8yptk7untd9hxwg3q2d6xjcmtv4ezq7pqxgsxzmnyyqcjqmt0wfjjq6t5v4khx"
                "sp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygsxqyjw5qcqp2rzjq0gxwkzc8w6323m55m4jyxcjwmy7stt9hwkwe"
                "2qxmy8zpsgg7jcuwz87fcqqeuqqqyqqqqlgqqqqn3qq9q9qrsgqrvgkpnmps664wgkp43l22qsgdw4ve24aca4nymnxddlnp8vh9v2sdxl"
                "u5ywdxefsfvm0fq3sesf08uf6q9a2ke0hc9j6z6wlxg5z5kqpu2v9wz",
                967_878_534,
                "bc",
                1572468703,
                "462264ede7e14047e9b249da94fefc47f41f7d02ee9b091815a5506bc8abf75f",
                "82",
                "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
                "1111111111111111111111111111111111111111111111111111111111111111",
                "1b1160cf6186b55722c1ac7ea502086baaccaabdc76b326e666b7f309d972b15069bfca11cd365304b36f48230cc12f3f13a017aab65f7c165a169df32282a58",
                "Blockstream Store: 88.85 USD for Blockstream Ledger Nano S x 1, \"Back In My Day\" "
                "Sticker x 2, \"I Got Lightning Working\" Sticker x 2 and 1 more items",
                None,
                604800,
            ),
            # (
            #     # Please send $30 for coffee beans to the same peer, which supports features 8, 14 and 99,
            #     # using secret 0x1111111111111111111111111111111111111111111111111111111111111111
            #     "invoice_11",
            #     "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetpdeessp5zyg3zyg"
            #     "3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqqsgq2a25dxl5hrntdtn6zvydt7d66hyzsyhqs4w"
            #     "dynavys42xgl6sgx9c4g7me86a27t07mdtfry458rtjr0v92cnmswpsjscgt2vcse3sgpz3uapa",
            #     2_500_000_000,
            #     "bc",
            #     1496314658,
            #     "462264ede7e14047e9b249da94fefc47f41f7d02ee9b091815a5506bc8abf75f",
            #     "82",
            #     "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            #     "1111111111111111111111111111111111111111111111111111111111111111",
            #     "5755469bf4b8e6b6ae7a1308d5f9bad5c82812e0855cd24fac242aa323fa820c5c551ede4faeabcb7fb6d5a464ad0e35c86f615589ee0e0c250c216a662198c1",
            #     "coffee beans",
            #     None,
            #     604800,
            # ),
            # (
            #     # Same, but all upper case.
            #     "invoice_12",
            #     "LNBC25M1PVJLUEZPP5QQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQYPQDQ5VDHKVEN9V5SXYETPDEESSP5ZYG3ZYG3ZYG3Z"
            #     "YG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYGS9Q5SQQQQQQQQQQQQQQQQSGQ2A25DXL5HRNTDTN6ZVYDT7D66HYZSYHQS4WDYNAVYS42XGL"
            #     "6SGX9C4G7ME86A27T07MDTFRY458RTJR0V92CNMSWPSJSCGT2VCSE3SGPZ3UAPA",
            #     2_500_000_000,
            #     "bc",
            #     1496314658,
            #     "0001020304050607080900010203040506070809000102030405060708090102",
            #     "800000000000000000000410",
            #     "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            #     "1111111111111111111111111111111111111111111111111111111111111111",
            #     "5755469bf4b8e6b6ae7a1308d5f9bad5c82812e0855cd24fac242aa323fa820c5c551ede4faeabcb7fb6d5a464ad0e35c86f615589ee0e0c250c216a662198c1",
            #     "coffee beans",
            #     None,
            #     604800,
            # ),
            # (
            #     # Same, but including fields which must be ignored.
            #     "invoice_13",
            #     "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetpdeessp5zyg3zyg3zyg3z"
            #     "yg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqqsgq2qrqqqfppnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqppnqq"
            #     "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqpp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqhpnq"
            #     "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqhp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqspn"
            #     "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqsp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnp"
            #     "5qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnpkqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
            #     "qz599y53s3ujmcfjp5xrdap68qxymkqphwsexhmhr8wdz5usdzkzrse33chw6dlp3jhuhge9ley7j2ayx36kawe7kmgg8sv5ugdyusdcqzn8z9x",
            #     2_500_000_000,
            #     "bc",
            #     1496314658,
            #     "462264ede7e14047e9b249da94fefc47f41f7d02ee9b091815a5506bc8abf75f",
            #     "82",
            #     "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            #     "1111111111111111111111111111111111111111111111111111111111111111",
            #     "5755469bf4b8e6b6ae7a1308d5f9bad5c82812e0855cd24fac242aa323fa820c5c551ede4faeabcb7fb6d5a464ad0e35c86f615589ee0e0c250c216a662198c1",
            #     "coffee beans",
            #     None,
            #     604800,
            # ),
        ],
    )
    def test_decode(
        self,
        name,
        payment_request,
        amount,
        currency,
        date,
        payment_hash,
        features,
        payee,
        payment_secret,
        signature,
        description,
        description_hash,
        expiry,
    ):

        print(f"decoding invoice: {name}")
        decoded = decode(payment_request)

        if amount:
            assert decoded.amount == amount
        assert decoded.currency == currency
        assert decoded.date == date
        assert decoded.payment_hash == payment_hash
        assert decoded.features == features
        assert decoded.payee == payee
        assert decoded.payment_secret == payment_secret
        assert decoded.signature == signature
        if description:
            assert decoded.description == description
        if description_hash:
            assert decoded.description_hash == description_hash
        assert decoded.expiry == expiry


# INVALID INVOICES
class TestDecodeFail:
    @pytest.mark.parametrize(
        "name, payment_request",
        [
            (
                # Same, but adding invalid unknown feature 100
                "fail_invoice_1",
                "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetpdeessp5zyg3zyg3zyg3z"
                "yg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q4psqqqqqqqqqqqqqqqqsgqtqyx5vggfcsll4wu246hz02kp85x4katwsk9639we5n5yn"
                "gc3yhqkm35jnjw4len8vrnqnf5ejh0mzj9n3vz2px97evektfm2l6wqccp3y7372",
            )
        ]
    )
    def test_decode_fail(self, name, payment_request):
        print(f"decoding fail invoice: {name}")
        decoded = decode(payment_request)
        print(decoded.json())

#
#
# Bech32 checksum is invalid.
# lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpuyk0sg5g70me25alkluzd2x62aysf2pyy8edtjeevuv4p2d5p76r4zkmneet7uvyakky2zr4cusd45tftc9c5fh0nnqpnl2jfll544esqchsrnt
#
# Malformed bech32 string (no 1)
# pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpuyk0sg5g70me25alkluzd2x62aysf2pyy8edtjeevuv4p2d5p76r4zkmneet7uvyakky2zr4cusd45tftc9c5fh0nnqpnl2jfll544esqchsrny
#
# Malformed bech32 string (mixed case)
# LNBC2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpuyk0sg5g70me25alkluzd2x62aysf2pyy8edtjeevuv4p2d5p76r4zkmneet7uvyakky2zr4cusd45tftc9c5fh0nnqpnl2jfll544esqchsrny
#
# Signature is not recoverable.
# lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpusp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9qrsgqwgt7mcn5yqw3yx0w94pswkpq6j9uh6xfqqqtsk4tnarugeektd4hg5975x9am52rz4qskukxdmjemg92vvqz8nvmsye63r5ykel43pgz7zq0g2
#
# String is too short.
# lnbc1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2ursdae8g6na6hlh
#
# Invalid multiplier
# lnbc2500x1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpusp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9qrsgqrrzc4cvfue4zp3hggxp47ag7xnrlr8vgcmkjxk3j5jqethnumgkpqp23z9jclu3v0a7e0aruz366e9wqdykw6dxhdzcjjhldxq0w6wgqcnu43j
#
# Invalid sub-millisatoshi precision.
# lnbc2500000001p1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpusp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9qrsgq0lzc236j96a95uv0m3umg28gclm5lqxtqqwk32uuk4k6673k6n5kfvx3d2h8s295fad45fdhmusm8sjudfhlf6dcsxmfvkeywmjdkxcp99202x
